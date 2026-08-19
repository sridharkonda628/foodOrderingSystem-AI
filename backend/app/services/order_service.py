"""
Order Processing Service and Strict State Machine.

Use Case:
- Manages complete customer order placement lifecycle:
  1. Cart validation & out-of-stock check.
  2. Server-side price calculation to prevent client tampering.
  3. Price snapshotting in order items table.
- Enforces strict order state machine progression (e.g. PLACED -> CONFIRMED -> PREPARING -> READY -> PICKED_UP).
- Enforces role-based permissions (customers can only cancel orders in 'placed' status; admins manage kitchen workflow).
"""

import uuid
from typing import List, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import (
    NotFoundException,
    ForbiddenException,
    ItemUnavailableException,
    InvalidStateTransitionException,
    BadRequestException
)
from app.models.order import Order, OrderItem, OrderStatus
from app.models.user import User, UserRole
from app.models.menu_item import MenuItem
from app.repositories.menu_repo import MenuRepository
from app.repositories.order_repo import OrderRepository
from app.schemas.order import OrderCreate


class OrderStateMachine:
    """
    Strict State Machine governing order lifecycle transitions.

    Use Case:
    - Guarantees valid kitchen workflow and prevents illegal state bypasses (e.g. PLACED -> READY).
    - Prevents modifications to terminal states (PICKED_UP and CANCELLED).
    """
    VALID_TRANSITIONS: Dict[str, List[str]] = {
        OrderStatus.PLACED.value: [
            OrderStatus.CONFIRMED.value,
            OrderStatus.CANCELLED.value
        ],
        OrderStatus.CONFIRMED.value: [
            OrderStatus.PREPARING.value,
            OrderStatus.CANCELLED.value
        ],
        OrderStatus.PREPARING.value: [
            OrderStatus.READY.value
        ],
        OrderStatus.READY.value: [
            OrderStatus.PICKED_UP.value
        ],
        OrderStatus.PICKED_UP.value: [],    # Terminal success state
        OrderStatus.CANCELLED.value: []     # Terminal abort state
    }

    @classmethod
    def can_transition(cls, current_status: str, target_status: str) -> bool:
        """
        Checks if transitioning from current_status to target_status is permitted.

        Parameters:
        - current_status: Existing order status string.
        - target_status: Desired new status string.

        Returns:
        - True if transition is valid, False otherwise.
        """
        allowed = cls.VALID_TRANSITIONS.get(current_status, [])
        return target_status in allowed

    @classmethod
    def validate_transition(cls, current_status: str, target_status: str):
        """
        Validates state transition and raises exception on violation.

        Parameters:
        - current_status: Existing order status string.
        - target_status: Desired new status string.

        Raises:
        - InvalidStateTransitionException: If transition is illegal.
        """
        if not cls.can_transition(current_status, target_status):
            allowed = cls.VALID_TRANSITIONS.get(current_status, [])
            allowed_str = ", ".join(allowed) if allowed else "none (terminal state)"
            raise InvalidStateTransitionException(
                f"Cannot transition order from '{current_status}' to '{target_status}'. "
                f"Allowed transitions: [{allowed_str}]."
            )


class OrderService:
    """
    Service handling checkout validation, order calculations, and status updates.
    """

    @staticmethod
    async def create_order(
        db: AsyncSession,
        customer: User,
        data: OrderCreate
    ) -> Order:
        """
        Creates a new customer order with server-side validation and price computation.

        Use Case:
        - Invoked when customer clicks "Checkout" on cart.
        - Steps:
          1. Fetches real-time dish records from DB to ensure prices cannot be manipulated on client.
          2. Verifies that all dishes are currently marked available (`is_available = True`).
          3. Validates positive quantities.
          4. Computes line item subtotals and order total amount.
          5. Stores immutable price snapshot records in `order_items`.

        Parameters:
        - db: The active async database session.
        - customer: Authenticated User entity.
        - data: Validated OrderCreate schema containing cart items and delivery notes.

        Returns:
        - Newly created Order entity with items populated.

        Raises:
        - BadRequestException: If order has no items or invalid quantities.
        - NotFoundException: If an item ID does not exist.
        - ItemUnavailableException: If any item in cart is currently out of stock.
        """
        if not data.items:
            raise BadRequestException("An order must contain at least one item.")

        # 1. Fetch all requested menu items from database in a single query
        requested_ids = [item_in.menu_item_id for item_in in data.items]
        menu_items_map: Dict[str, MenuItem] = {
            item.id: item for item in await MenuRepository.get_items_by_ids(db, requested_ids)
        }

        # 2. Validate availability and calculate price integrity
        order_id = str(uuid.uuid4())
        order_items_to_create: List[OrderItem] = []
        total_amount: float = 0.0

        for item_in in data.items:
            item_entity = menu_items_map.get(item_in.menu_item_id)
            if not item_entity:
                raise NotFoundException(f"Menu item id '{item_in.menu_item_id}' not found.")
            
            # Reject checkout if item is 86'd / out of stock
            if not item_entity.is_available:
                raise ItemUnavailableException(
                    f"'{item_entity.name}' is currently unavailable. Please remove it from your cart to proceed."
                )

            if item_in.quantity <= 0:
                raise BadRequestException(f"Invalid quantity {item_in.quantity} for '{item_entity.name}'.")

            unit_price = item_entity.price
            subtotal = round(unit_price * item_in.quantity, 2)
            total_amount += subtotal

            order_item = OrderItem(
                id=str(uuid.uuid4()),
                order_id=order_id,
                menu_item_id=item_entity.id,
                quantity=item_in.quantity,
                unit_price=unit_price,
                subtotal=subtotal
            )
            order_items_to_create.append(order_item)

        # 3. Create parent Order entity
        order = Order(
            id=order_id,
            customer_id=customer.id,
            status=OrderStatus.PLACED.value,
            total_amount=round(total_amount, 2),
            delivery_notes=data.delivery_notes.strip() if data.delivery_notes else ""
        )

        created_order = await OrderRepository.create_order(db, order, order_items_to_create)
        return created_order

    @staticmethod
    async def get_customer_orders(
        db: AsyncSession,
        customer_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[Order]:
        """
        Retrieves order history for a customer.

        Use Case:
        - Powers the customer "My Orders" history page.

        Parameters:
        - db: The active async database session.
        - customer_id: UUID string of the customer.
        - limit: Maximum records to return.
        - offset: Pagination offset.

        Returns:
        - List of Order entities.
        """
        return await OrderRepository.get_customer_orders(db, customer_id, limit, offset)

    @staticmethod
    async def get_order_by_id(
        db: AsyncSession,
        order_id: str,
        current_user: User
    ) -> Order:
        """
        Retrieves a single order by ID with ownership authorization check.

        Use Case:
        - Customers can only view their own orders; Admins can view any restaurant order.

        Parameters:
        - db: The active async database session.
        - order_id: UUID string of the order.
        - current_user: Authenticated user entity.

        Returns:
        - Order entity.

        Raises:
        - NotFoundException: If order does not exist.
        - ForbiddenException: If customer attempts to access someone else's order.
        """
        order = await OrderRepository.get_by_id(db, order_id)
        if not order:
            raise NotFoundException(f"Order with id '{order_id}' was not found.")

        if current_user.role != UserRole.ADMIN.value and order.customer_id != current_user.id:
            raise ForbiddenException("You do not have permission to view this order.")

        return order

    @staticmethod
    async def get_all_orders_for_admin(
        db: AsyncSession,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Order]:
        """
        Retrieves all restaurant orders for admin overview.

        Use Case:
        - Admin Order Management dashboard with optional status filter tabs.

        Parameters:
        - db: The active async database session.
        - status: Optional status filter.
        - limit: Maximum records.
        - offset: Pagination offset.

        Returns:
        - List of Order entities.
        """
        return await OrderRepository.get_all_orders(db, status, limit, offset)

    @staticmethod
    async def update_order_status(
        db: AsyncSession,
        order_id: str,
        new_status: str,
        current_user: User
    ) -> Order:
        """
        Updates order status with permission checks and state machine validation.

        Use Case:
        - Progresses order through lifecycle states (admin), or cancels placed order (customer).

        Parameters:
        - db: The active async database session.
        - order_id: UUID string of the order.
        - new_status: Target status string.
        - current_user: Authenticated user.

        Returns:
        - Updated Order entity.

        Raises:
        - NotFoundException: If order does not exist.
        - ForbiddenException: If customer attempts unauthorized state change or accesses another's order.
        - InvalidStateTransitionException: If transition violates OrderStateMachine rules.
        """
        order = await OrderRepository.get_by_id(db, order_id)
        if not order:
            raise NotFoundException(f"Order with id '{order_id}' was not found.")

        # Customer authorization restrictions
        if current_user.role != UserRole.ADMIN.value:
            if order.customer_id != current_user.id:
                raise ForbiddenException("You do not have permission to update this order.")
            if new_status != OrderStatus.CANCELLED.value:
                raise ForbiddenException("Customers can only cancel orders.")
            if order.status != OrderStatus.PLACED.value:
                raise InvalidStateTransitionException("Orders can only be cancelled while in 'placed' status.")

        # Validate transition against strict state machine
        OrderStateMachine.validate_transition(order.status, new_status)
        updated_order = await OrderRepository.update_status(db, order, new_status)
        return updated_order
