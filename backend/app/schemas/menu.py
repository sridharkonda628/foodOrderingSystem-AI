from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    slug: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None
    display_order: int = 0
    is_active: bool = True


class CategoryCreate(CategoryBase):
    pass


class CategoryOut(CategoryBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MenuItemBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    description: str = Field("", max_length=1000)
    category_id: int
    price: float = Field(..., gt=0, description="Price in INR")
    is_vegetarian: bool = True
    is_spicy: bool = False
    dietary_tags: List[str] = Field(default_factory=list)
    is_available: bool = True


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    price: Optional[float] = Field(None, gt=0)
    is_vegetarian: Optional[bool] = None
    is_spicy: Optional[bool] = None
    dietary_tags: Optional[List[str]] = None
    is_available: Optional[bool] = None


class AvailabilityToggle(BaseModel):
    is_available: bool


class MenuItemOut(MenuItemBase):
    id: str
    popularity_score: float
    category_name: Optional[str] = None
    category_slug: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
