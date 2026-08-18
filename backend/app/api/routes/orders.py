from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.common import APIResponse
from app.schemas.order import OrderCreate, OrderOut, OrderItemOut
from app.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["Orders"])


def _format_order_out(order) -> OrderOut:
    items_out = []
    for it in order.items:
        item_name = it.menu_item.name if it.menu_item else "Unknown Item"
        is_veg = it.menu_item.is_vegetarian if it.menu_item else True
        items_out.append(
            OrderItemOut(
                id=it.id,
                menu_item_id=it.menu_item_id,
                menu_item_name=item_name,
                quantity=it.quantity,
                unit_price=it.unit_price,
                subtotal=it.subtotal,
                is_vegetarian=is_veg
            )
        )
    return OrderOut(
        id=order.id,
        customer_id=order.customer_id,
        customer_name=order.customer.full_name if order.customer else None,
        customer_email=order.customer.email if order.customer else None,
        status=order.status,
        total_amount=order.total_amount,
        delivery_notes=order.delivery_notes,
        created_at=order.created_at,
        updated_at=order.updated_at,
        items=items_out
    )


@router.post("", response_model=APIResponse[OrderOut], status_code=status.HTTP_201_CREATED)
async def create_order(
    data: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = await OrderService.create_order(db, current_user, data)
    return APIResponse(
        success=True,
        data=_format_order_out(order),
        message="Order placed successfully"
    )


@router.get("", response_model=APIResponse[List[OrderOut]])
async def get_my_orders(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    orders = await OrderService.get_customer_orders(db, current_user.id)
    data = [_format_order_out(o) for o in orders]
    return APIResponse(
        success=True,
        data=data,
        message="Customer orders retrieved"
    )


@router.get("/{order_id}", response_model=APIResponse[OrderOut])
async def get_order_by_id(
    order_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = await OrderService.get_order_by_id(db, order_id, current_user)
    return APIResponse(
        success=True,
        data=_format_order_out(order),
        message="Order retrieved"
    )


@router.patch("/{order_id}/cancel", response_model=APIResponse[OrderOut])
async def cancel_my_order(
    order_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = await OrderService.update_order_status(db, order_id, "cancelled", current_user)
    return APIResponse(
        success=True,
        data=_format_order_out(order),
        message="Order cancelled"
    )
