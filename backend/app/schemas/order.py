"""
Order and Order Item Pydantic Schemas.

Use Case:
- Validates order placement requests (`OrderCreate`, `OrderItemCreate`).
- Serializes order history, status updates, and line item breakdowns (`OrderOut`, `OrderItemOut`).
- Validates admin/customer status updates (`OrderStatusUpdate`).
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from app.models.order import OrderStatus


class OrderItemCreate(BaseModel):
    """
    Request schema for an individual item inside an order checkout payload.

    Use Case: Specifies the menu item ID and desired quantity.
    """
    menu_item_id: str
    quantity: int = Field(..., ge=1, description="Quantity must be at least 1")


class OrderCreate(BaseModel):
    """
    Request schema for customer checkout.

    Use Case: Submits the list of cart items and optional delivery instructions.
    """
    items: List[OrderItemCreate] = Field(..., min_length=1, description="Order must have at least one item")
    delivery_notes: Optional[str] = Field("", max_length=500)


class OrderItemOut(BaseModel):
    """
    Response schema for an item within a retrieved order.

    Use Case: Serializes item quantity, unit price snapshot, subtotal, and dish name.
    """
    id: str
    menu_item_id: str
    menu_item_name: str
    quantity: int
    unit_price: float
    subtotal: float
    is_vegetarian: Optional[bool] = True

    model_config = ConfigDict(from_attributes=True)


class OrderOut(BaseModel):
    """
    Response schema representing complete order information.

    Use Case: Returned to customers on their order tracking page and to admins on order management page.
    """
    id: str
    customer_id: str
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    status: str
    total_amount: float
    delivery_notes: Optional[str] = ""
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemOut] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class OrderStatusUpdate(BaseModel):
    """
    Request schema for order state transitions.

    Use Case: Used by admin to update workflow status (e.g. placed -> preparing -> ready).
    """
    status: OrderStatus
