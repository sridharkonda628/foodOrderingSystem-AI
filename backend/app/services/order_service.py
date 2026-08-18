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
    Strict state machine governing order transitions.
    Disallows illegal shortcuts such as PLACED -> READY.
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
        OrderStatus.PICKED_UP.value: [],
        OrderStatus.CANCELLED.value: []
    }

    @classmethod
    def can_transition(cls, current_status: str, target_status: str) -> bool:
        allowed = cls.VALID_TRANSITIONS.get(current_status, [])
        return target_status in allowed

    @classmethod
    def validate_transition(cls, current_status: str, target_status: str):
        if not cls.can_transition(current_status, target_status):
            allowed = cls.VALID_TRANSITIONS.get(current_status, [])
            allowed_str = ", ".join(allowed) if allowed else "none (terminal state)"
            raise InvalidStateTransitionException(
                f"Cannot transition order from '{current_status}' to '{target_status}'. "
                f"Allowed transitions: [{allowed_str}]."
            )


class OrderService:
    @staticmethod
    async def create_order(
        db: AsyncSession,
        customer: User,
        data: OrderCreate
    ) -> Order:
        if not data.items:
            raise BadRequestException("An order must contain at least one item.")

        # 1. Fetch all requested menu items from database
        requested_ids = [item_in.menu_item_id for item_in in data.items]
        menu_items_map: Dict[str, MenuItem] = {
            item.id: item for item in await MenuRepository.get_items_by_ids(db, requested_ids)
        }

        # 2. Validate availability and price integrity
        order_id = str(uuid.uuid4())
        order_items_to_create: List[OrderItem] = []
        total_amount: float = 0.0

        for item_in in data.items:
            item_entity = menu_items_map.get(item_in.menu_item_id)
            if not item_entity:
                raise NotFoundException(f"Menu item id '{item_in.menu_item_id}' not found.")
            
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
        return await OrderRepository.get_customer_orders(db, customer_id, limit, offset)

    @staticmethod
    async def get_order_by_id(
        db: AsyncSession,
        order_id: str,
        current_user: User
    ) -> Order:
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
        return await OrderRepository.get_all_orders(db, status, limit, offset)

    @staticmethod
    async def update_order_status(
        db: AsyncSession,
        order_id: str,
        new_status: str,
        current_user: User
    ) -> Order:
        order = await OrderRepository.get_by_id(db, order_id)
        if not order:
            raise NotFoundException(f"Order with id '{order_id}' was not found.")

        if current_user.role != UserRole.ADMIN.value:
            if order.customer_id != current_user.id:
                raise ForbiddenException("You do not have permission to update this order.")
            if new_status != OrderStatus.CANCELLED.value:
                raise ForbiddenException("Customers can only cancel orders.")
            if order.status != OrderStatus.PLACED.value:
                raise InvalidStateTransitionException("Orders can only be cancelled while in 'placed' status.")

        OrderStateMachine.validate_transition(order.status, new_status)
        updated_order = await OrderRepository.update_status(db, order, new_status)
        return updated_order
