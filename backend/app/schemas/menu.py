"""
Category and Menu Item Pydantic Schemas.

Use Case:
- Validates data for creating and updating menu categories (`CategoryCreate`, `CategoryOut`).
- Validates data for creating, updating, toggling availability, and serializing dishes
  (`MenuItemCreate`, `MenuItemUpdate`, `AvailabilityToggle`, `MenuItemOut`).
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class CategoryBase(BaseModel):
    """
    Shared fields for menu category models.
    """
    name: str = Field(..., min_length=2, max_length=100)
    slug: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None
    display_order: int = 0
    is_active: bool = True


class CategoryCreate(CategoryBase):
    """
    Request schema for creating a new menu category.

    Use Case: Validates admin inputs when adding a new category.
    """
    pass


class CategoryOut(CategoryBase):
    """
    Response schema for category entity.

    Use Case: Serializes category list for customer browsing and admin configuration.
    """
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MenuItemBase(BaseModel):
    """
    Shared fields for menu dish items.
    """
    name: str = Field(..., min_length=2, max_length=200)
    description: str = Field("", max_length=1000)
    category_id: int
    price: float = Field(..., gt=0, description="Price in INR")
    is_vegetarian: bool = True
    is_spicy: bool = False
    dietary_tags: List[str] = Field(default_factory=list)
    is_available: bool = True


class MenuItemCreate(MenuItemBase):
    """
    Request schema for adding a new dish to the menu.

    Use Case: Used by admin to introduce new menu items.
    """
    pass


class MenuItemUpdate(BaseModel):
    """
    Request schema for updating an existing dish.

    Use Case: Allows partial updates to dish details, pricing, tags, or availability.
    """
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    price: Optional[float] = Field(None, gt=0)
    is_vegetarian: Optional[bool] = None
    is_spicy: Optional[bool] = None
    dietary_tags: Optional[List[str]] = None
    is_available: Optional[bool] = None


class AvailabilityToggle(BaseModel):
    """
    Request schema for quickly toggling 86'd / out-of-stock items.

    Use Case: Used by kitchen staff/admin to instantly mark dishes available or unavailable.
    """
    is_available: bool


class MenuItemOut(MenuItemBase):
    """
    Response schema for menu dish details.

    Use Case: Serializes dish attributes with category relationship context.
    """
    id: str
    popularity_score: float
    category_name: Optional[str] = None
    category_slug: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
