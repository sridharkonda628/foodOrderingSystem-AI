from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import NotFoundException, ConflictException
from app.models.category import Category
from app.models.menu_item import MenuItem
from app.repositories.menu_repo import MenuRepository
from app.schemas.menu import MenuItemCreate, MenuItemUpdate, CategoryCreate


class MenuService:
    @staticmethod
    async def get_categories(db: AsyncSession, active_only: bool = True) -> List[Category]:
        return await MenuRepository.get_categories(db, active_only=active_only)

    @staticmethod
    async def create_category(db: AsyncSession, data: CategoryCreate) -> Category:
        existing = await MenuRepository.get_category_by_slug(db, data.slug)
        if existing:
            raise ConflictException(f"Category slug '{data.slug}' already exists.")
        
        category = Category(
            name=data.name.strip(),
            slug=data.slug.lower().strip(),
            description=data.description,
            display_order=data.display_order,
            is_active=data.is_active
        )
        return await MenuRepository.create_category(db, category)

    @staticmethod
    async def get_menu_items(
        db: AsyncSession,
        category_id: Optional[int] = None,
        is_vegetarian: Optional[bool] = None,
        is_spicy: Optional[bool] = None,
        available_only: bool = False,
        limit: int = 100,
        offset: int = 0
    ) -> List[MenuItem]:
        return await MenuRepository.get_items(
            db,
            category_id=category_id,
            is_vegetarian=is_vegetarian,
            is_spicy=is_spicy,
            available_only=available_only,
            limit=limit,
            offset=offset
        )

    @staticmethod
    async def get_menu_item(db: AsyncSession, item_id: str) -> MenuItem:
        item = await MenuRepository.get_item_by_id(db, item_id)
        if not item:
            raise NotFoundException(f"Menu item with id '{item_id}' was not found.")
        return item

    @staticmethod
    async def create_menu_item(db: AsyncSession, data: MenuItemCreate) -> MenuItem:
        category = await MenuRepository.get_category_by_id(db, data.category_id)
        if not category:
            raise NotFoundException(f"Category id {data.category_id} not found.")

        item = MenuItem(
            category_id=data.category_id,
            name=data.name.strip(),
            description=data.description.strip(),
            price=round(float(data.price), 2),
            is_vegetarian=data.is_vegetarian,
            is_spicy=data.is_spicy,
            dietary_tags=[t.lower().strip() for t in data.dietary_tags],
            is_available=data.is_available,
            popularity_score=0.0
        )
        return await MenuRepository.create_item(db, item)

    @staticmethod
    async def update_menu_item(db: AsyncSession, item_id: str, data: MenuItemUpdate) -> MenuItem:
        item = await MenuRepository.get_item_by_id(db, item_id)
        if not item:
            raise NotFoundException(f"Menu item with id '{item_id}' not found.")

        if data.category_id is not None:
            category = await MenuRepository.get_category_by_id(db, data.category_id)
            if not category:
                raise NotFoundException(f"Category id {data.category_id} not found.")
            item.category_id = data.category_id

        if data.name is not None:
            item.name = data.name.strip()
        if data.description is not None:
            item.description = data.description.strip()
        if data.price is not None:
            item.price = round(float(data.price), 2)
        if data.is_vegetarian is not None:
            item.is_vegetarian = data.is_vegetarian
        if data.is_spicy is not None:
            item.is_spicy = data.is_spicy
        if data.dietary_tags is not None:
            item.dietary_tags = [t.lower().strip() for t in data.dietary_tags]
        if data.is_available is not None:
            item.is_available = data.is_available

        return await MenuRepository.update_item(db, item)

    @staticmethod
    async def toggle_availability(db: AsyncSession, item_id: str, is_available: bool) -> MenuItem:
        item = await MenuRepository.get_item_by_id(db, item_id)
        if not item:
            raise NotFoundException(f"Menu item with id '{item_id}' not found.")
        item.is_available = is_available
        return await MenuRepository.update_item(db, item)

    @staticmethod
    async def delete_menu_item(db: AsyncSession, item_id: str) -> None:
        item = await MenuRepository.get_item_by_id(db, item_id)
        if not item:
            raise NotFoundException(f"Menu item with id '{item_id}' not found.")
        await MenuRepository.delete_item(db, item)
