from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from app.models.order import OrderStatus


class OrderItemCreate(BaseModel):
    menu_item_id: str
    quantity: int = Field(..., ge=1, description="Quantity must be at least 1")


class OrderCreate(BaseModel):
    items: List[OrderItemCreate] = Field(..., min_length=1, description="Order must have at least one item")
    delivery_notes: Optional[str] = Field("", max_length=500)


class OrderItemOut(BaseModel):
    id: str
    menu_item_id: str
    menu_item_name: str
    quantity: int
    unit_price: float
    subtotal: float
    is_vegetarian: Optional[bool] = True

    model_config = ConfigDict(from_attributes=True)


class OrderOut(BaseModel):
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
    status: OrderStatus
