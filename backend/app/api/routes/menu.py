from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_active_admin
from app.models.user import User
from app.schemas.common import APIResponse
from app.schemas.menu import (
    CategoryCreate,
    CategoryOut,
    MenuItemCreate,
    MenuItemUpdate,
    MenuItemOut,
    AvailabilityToggle
)
from app.services.menu_service import MenuService

router = APIRouter(prefix="/menu", tags=["Menu Management"])


# Categories Endpoints
@router.get("/categories", response_model=APIResponse[List[CategoryOut]])
async def list_categories(
    active_only: bool = Query(True),
    db: AsyncSession = Depends(get_db)
):
    categories = await MenuService.get_categories(db, active_only=active_only)
    data = [CategoryOut.model_validate(c) for c in categories]
    return APIResponse(success=True, data=data, message="Categories retrieved")


@router.post("/categories", response_model=APIResponse[CategoryOut], status_code=status.HTTP_201_CREATED)
async def create_category(
    data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_active_admin)
):
    cat = await MenuService.create_category(db, data)
    return APIResponse(success=True, data=CategoryOut.model_validate(cat), message="Category created")


# Menu Items Endpoints
@router.get("", response_model=APIResponse[List[MenuItemOut]])
async def list_menu_items(
    category_id: Optional[int] = Query(None),
    is_vegetarian: Optional[bool] = Query(None),
    is_spicy: Optional[bool] = Query(None),
    available_only: bool = Query(False),
    limit: int = Query(100, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    items = await MenuService.get_menu_items(
        db=db,
        category_id=category_id,
        is_vegetarian=is_vegetarian,
        is_spicy=is_spicy,
        available_only=available_only,
        limit=limit,
        offset=offset
    )
    result = []
    for it in items:
        out = MenuItemOut(
            id=it.id,
            name=it.name,
            description=it.description,
            category_id=it.category_id,
            category_name=it.category.name if it.category else None,
            category_slug=it.category.slug if it.category else None,
            price=it.price,
            is_vegetarian=it.is_vegetarian,
            is_spicy=it.is_spicy,
            dietary_tags=it.dietary_tags,
            is_available=it.is_available,
            popularity_score=it.popularity_score,
            created_at=it.created_at,
            updated_at=it.updated_at
        )
        result.append(out)
    return APIResponse(success=True, data=result, message="Menu items retrieved")


@router.get("/{item_id}", response_model=APIResponse[MenuItemOut])
async def get_menu_item(
    item_id: str,
    db: AsyncSession = Depends(get_db)
):
    it = await MenuService.get_menu_item(db, item_id)
    out = MenuItemOut(
        id=it.id,
        name=it.name,
        description=it.description,
        category_id=it.category_id,
        category_name=it.category.name if it.category else None,
        category_slug=it.category.slug if it.category else None,
        price=it.price,
        is_vegetarian=it.is_vegetarian,
        is_spicy=it.is_spicy,
        dietary_tags=it.dietary_tags,
        is_available=it.is_available,
        popularity_score=it.popularity_score,
        created_at=it.created_at,
        updated_at=it.updated_at
    )
    return APIResponse(success=True, data=out, message="Item retrieved")


@router.post("", response_model=APIResponse[MenuItemOut], status_code=status.HTTP_201_CREATED)
async def create_menu_item(
    data: MenuItemCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_active_admin)
):
    it = await MenuService.create_menu_item(db, data)
    out = MenuItemOut(
        id=it.id,
        name=it.name,
        description=it.description,
        category_id=it.category_id,
        category_name=it.category.name if it.category else None,
        category_slug=it.category.slug if it.category else None,
        price=it.price,
        is_vegetarian=it.is_vegetarian,
        is_spicy=it.is_spicy,
        dietary_tags=it.dietary_tags,
        is_available=it.is_available,
        popularity_score=it.popularity_score,
        created_at=it.created_at,
        updated_at=it.updated_at
    )
    return APIResponse(success=True, data=out, message="Menu item created")


@router.put("/{item_id}", response_model=APIResponse[MenuItemOut])
async def update_menu_item(
    item_id: str,
    data: MenuItemUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_active_admin)
):
    it = await MenuService.update_menu_item(db, item_id, data)
    out = MenuItemOut(
        id=it.id,
        name=it.name,
        description=it.description,
        category_id=it.category_id,
        category_name=it.category.name if it.category else None,
        category_slug=it.category.slug if it.category else None,
        price=it.price,
        is_vegetarian=it.is_vegetarian,
        is_spicy=it.is_spicy,
        dietary_tags=it.dietary_tags,
        is_available=it.is_available,
        popularity_score=it.popularity_score,
        created_at=it.created_at,
        updated_at=it.updated_at
    )
    return APIResponse(success=True, data=out, message="Menu item updated")


@router.patch("/{item_id}/availability", response_model=APIResponse[MenuItemOut])
async def toggle_item_availability(
    item_id: str,
    data: AvailabilityToggle,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_active_admin)
):
    it = await MenuService.toggle_availability(db, item_id, data.is_available)
    out = MenuItemOut(
        id=it.id,
        name=it.name,
        description=it.description,
        category_id=it.category_id,
        category_name=it.category.name if it.category else None,
        category_slug=it.category.slug if it.category else None,
        price=it.price,
        is_vegetarian=it.is_vegetarian,
        is_spicy=it.is_spicy,
        dietary_tags=it.dietary_tags,
        is_available=it.is_available,
        popularity_score=it.popularity_score,
        created_at=it.created_at,
        updated_at=it.updated_at
    )
    return APIResponse(success=True, data=out, message=f"Availability set to {data.is_available}")


@router.delete("/{item_id}", response_model=APIResponse[dict])
async def delete_menu_item(
    item_id: str,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_active_admin)
):
    await MenuService.delete_menu_item(db, item_id)
    return APIResponse(success=True, data={"id": item_id}, message="Menu item deleted")
