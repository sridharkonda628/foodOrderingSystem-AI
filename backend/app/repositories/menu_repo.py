from typing import List, Optional
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.category import Category
from app.models.menu_item import MenuItem


class MenuRepository:
    # Categories
    @staticmethod
    async def get_categories(db: AsyncSession, active_only: bool = True) -> List[Category]:
        stmt = select(Category).order_by(Category.display_order.asc(), Category.name.asc())
        if active_only:
            stmt = stmt.where(Category.is_active.is_(True))
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def get_category_by_id(db: AsyncSession, category_id: int) -> Optional[Category]:
        stmt = select(Category).where(Category.id == category_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_category_by_slug(db: AsyncSession, slug: str) -> Optional[Category]:
        stmt = select(Category).where(Category.slug == slug.lower().strip())
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def create_category(db: AsyncSession, category: Category) -> Category:
        db.add(category)
        await db.commit()
        await db.refresh(category)
        return category

    # Menu Items
    @staticmethod
    async def get_items(
        db: AsyncSession,
        category_id: Optional[int] = None,
        is_vegetarian: Optional[bool] = None,
        is_spicy: Optional[bool] = None,
        available_only: bool = False,
        limit: int = 100,
        offset: int = 0
    ) -> List[MenuItem]:
        stmt = select(MenuItem).options(selectinload(MenuItem.category)).order_by(MenuItem.name.asc())
        
        if category_id is not None:
            stmt = stmt.where(MenuItem.category_id == category_id)
        if is_vegetarian is not None:
            stmt = stmt.where(MenuItem.is_vegetarian.is_(is_vegetarian))
        if is_spicy is not None:
            stmt = stmt.where(MenuItem.is_spicy.is_(is_spicy))
        if available_only:
            stmt = stmt.where(MenuItem.is_available.is_(True))

        stmt = stmt.limit(limit).offset(offset)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def get_item_by_id(db: AsyncSession, item_id: str) -> Optional[MenuItem]:
        stmt = select(MenuItem).options(selectinload(MenuItem.category)).where(MenuItem.id == item_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_items_by_ids(db: AsyncSession, item_ids: List[str]) -> List[MenuItem]:
        if not item_ids:
            return []
        stmt = select(MenuItem).options(selectinload(MenuItem.category)).where(MenuItem.id.in_(item_ids))
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def create_item(db: AsyncSession, item: MenuItem) -> MenuItem:
        db.add(item)
        await db.commit()
        await db.refresh(item)
        # Reload category relationship
        stmt = select(MenuItem).options(selectinload(MenuItem.category)).where(MenuItem.id == item.id)
        res = await db.execute(stmt)
        return res.scalar_one()

    @staticmethod
    async def update_item(db: AsyncSession, item: MenuItem) -> MenuItem:
        await db.commit()
        await db.refresh(item)
        stmt = select(MenuItem).options(selectinload(MenuItem.category)).where(MenuItem.id == item.id)
        res = await db.execute(stmt)
        return res.scalar_one()

    @staticmethod
    async def delete_item(db: AsyncSession, item: MenuItem) -> None:
        await db.delete(item)
        await db.commit()

    @staticmethod
    async def get_search_candidates(
        db: AsyncSession,
        max_price: Optional[float] = None,
        is_vegetarian: Optional[bool] = None,
        is_spicy: Optional[bool] = None,
        category_id: Optional[int] = None
    ) -> List[MenuItem]:
        # Always require is_available = True for search results
        stmt = select(MenuItem).options(selectinload(MenuItem.category)).where(MenuItem.is_available.is_(True))
        
        if max_price is not None:
            stmt = stmt.where(MenuItem.price <= max_price)
        if is_vegetarian is not None:
            stmt = stmt.where(MenuItem.is_vegetarian.is_(is_vegetarian))
        if is_spicy is not None:
            stmt = stmt.where(MenuItem.is_spicy.is_(is_spicy))
        if category_id is not None:
            stmt = stmt.where(MenuItem.category_id == category_id)

        result = await db.execute(stmt)
        return list(result.scalars().all())
