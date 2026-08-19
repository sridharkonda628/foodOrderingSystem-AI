"""
Menu and Category Repository.

Use Case:
- Encapsulates all raw database queries and operations for Categories and Menu Items.
- Isolates SQLAlchemy query construction (filtering, joins, sorting, pagination) from business logic services.
"""

from typing import List, Optional
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.category import Category
from app.models.menu_item import MenuItem


class MenuRepository:
    """
    Repository handling persistence and queries for Menu Items and Categories.
    """

    # -------------------------------------------------------------------------
    # Category Database Operations
    # -------------------------------------------------------------------------

    @staticmethod
    async def get_categories(db: AsyncSession, active_only: bool = True) -> List[Category]:
        """
        Retrieves all menu categories ordered by display priority.

        Use Case:
        - Fetches category navigation lists for the customer storefront and admin dashboard.

        Parameters:
        - db: The active async database session.
        - active_only: If True, filters only active categories.

        Returns:
        - List of Category entities.
        """
        stmt = select(Category).order_by(Category.display_order.asc(), Category.name.asc())
        if active_only:
            stmt = stmt.where(Category.is_active.is_(True))
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def get_category_by_id(db: AsyncSession, category_id: int) -> Optional[Category]:
        """
        Retrieves a category by its primary key ID.

        Use Case:
        - Validates existence when creating or updating menu items assigned to this category.

        Parameters:
        - db: The active async database session.
        - category_id: Integer primary key ID.

        Returns:
        - Category entity if found, None otherwise.
        """
        stmt = select(Category).where(Category.id == category_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_category_by_slug(db: AsyncSession, slug: str) -> Optional[Category]:
        """
        Retrieves a category by its unique URL slug.

        Use Case:
        - Checks for slug collisions before creating new categories or resolves categories by URL path.

        Parameters:
        - db: The active async database session.
        - slug: Unique category identifier string (e.g., 'starters').

        Returns:
        - Category entity if found, None otherwise.
        """
        stmt = select(Category).where(Category.slug == slug.lower().strip())
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def create_category(db: AsyncSession, category: Category) -> Category:
        """
        Inserts and commits a new Category entity.

        Use Case:
        - Used by admin to add a new category to the menu.

        Parameters:
        - db: The active async database session.
        - category: Unpersisted Category instance.

        Returns:
        - Persisted Category with auto-generated ID.
        """
        db.add(category)
        await db.commit()
        await db.refresh(category)
        return category

    # -------------------------------------------------------------------------
    # Menu Item Database Operations
    # -------------------------------------------------------------------------

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
        """
        Retrieves filtered and paginated menu items with category relationship eagerly loaded.

        Use Case:
        - Powers the customer menu browsing screen with multi-facet filters (category, veg, spicy, available).

        Parameters:
        - db: The active async database session.
        - category_id: Optional category ID filter.
        - is_vegetarian: Optional boolean filter for veg / non-veg dishes.
        - is_spicy: Optional boolean filter for spiciness.
        - available_only: If True, excludes out-of-stock dishes.
        - limit: Maximum number of items to return.
        - offset: Pagination offset.

        Returns:
        - List of MenuItem entities.
        """
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
        """
        Retrieves a single menu item by ID along with its category details.

        Use Case:
        - Used for dish detail view, cart item validation, and editing existing dishes.

        Parameters:
        - db: The active async database session.
        - item_id: UUID string of the menu item.

        Returns:
        - MenuItem entity if found, None otherwise.
        """
        stmt = select(MenuItem).options(selectinload(MenuItem.category)).where(MenuItem.id == item_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_items_by_ids(db: AsyncSession, item_ids: List[str]) -> List[MenuItem]:
        """
        Batch retrieves multiple menu items by a list of IDs.

        Use Case:
        - Used during order checkout to fetch and validate all cart items in a single efficient query.

        Parameters:
        - db: The active async database session.
        - item_ids: List of UUID strings.

        Returns:
        - List of matching MenuItem entities.
        """
        if not item_ids:
            return []
        stmt = select(MenuItem).options(selectinload(MenuItem.category)).where(MenuItem.id.in_(item_ids))
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def create_item(db: AsyncSession, item: MenuItem) -> MenuItem:
        """
        Inserts a new MenuItem and eagerly loads its category.

        Use Case:
        - Admin menu management: adding a new dish.

        Parameters:
        - db: The active async database session.
        - item: Unpersisted MenuItem entity.

        Returns:
        - Fully refreshed MenuItem with category details loaded.
        """
        db.add(item)
        await db.commit()
        await db.refresh(item)
        stmt = select(MenuItem).options(selectinload(MenuItem.category)).where(MenuItem.id == item.id)
        res = await db.execute(stmt)
        return res.scalar_one()

    @staticmethod
    async def update_item(db: AsyncSession, item: MenuItem) -> MenuItem:
        """
        Commits updates to an existing MenuItem entity.

        Use Case:
        - Admin menu management: updating dish name, description, price, or availability status.

        Parameters:
        - db: The active async database session.
        - item: Modified MenuItem instance.

        Returns:
        - Updated MenuItem entity.
        """
        await db.commit()
        await db.refresh(item)
        stmt = select(MenuItem).options(selectinload(MenuItem.category)).where(MenuItem.id == item.id)
        res = await db.execute(stmt)
        return res.scalar_one()

    @staticmethod
    async def delete_item(db: AsyncSession, item: MenuItem) -> None:
        """
        Deletes a MenuItem entity from the database.

        Use Case:
        - Admin menu management: removing a dish from the menu.

        Parameters:
        - db: The active async database session.
        - item: The MenuItem entity to delete.
        """
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
        """
        Retrieves candidate dishes matching hard constraints for AI NLP ranking.

        Use Case:
        - First phase of AI Hybrid Search pipeline: efficiently narrows down database items
          using strict boolean/price filters before computing multi-signal relevance scoring.
        - Enforces that only currently available items (`is_available = True`) are returned.

        Parameters:
        - db: The active async database session.
        - max_price: Optional upper price ceiling extracted from natural language (e.g. under 200).
        - is_vegetarian: Optional vegetarian constraint extracted from natural language.
        - is_spicy: Optional spiciness constraint.
        - category_id: Optional specific category constraint.

        Returns:
        - List of candidate MenuItem entities for ranking.
        """
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
