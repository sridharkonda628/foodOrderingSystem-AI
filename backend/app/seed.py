import asyncio
from datetime import datetime, timezone, timedelta
from app.core.security import get_password_hash
from app.db.session import engine, init_db, AsyncSessionLocal
from app.models.user import User, UserRole
from app.models.category import Category
from app.models.menu_item import MenuItem
from app.models.order import Order, OrderItem, OrderStatus
from sqlalchemy import select


async def seed_data():
    print("Connecting to database and creating tables...")
    await init_db()

    async with AsyncSessionLocal() as session:
        # Check if already seeded
        result = await session.execute(select(User).limit(1))
        if result.scalar_one_or_none():
            print("Database already contains data. Skipping initial seeding.")
            return

        print("Seeding Users...")
        # 1. Users
        admin_user = User(
            email="admin@kpitech.com",
            hashed_password=get_password_hash("AdminPass123!"),
            full_name="Restaurant Manager (Admin)",
            role=UserRole.ADMIN.value,
            is_active=True
        )
        customer_user = User(
            email="customer@example.com",
            hashed_password=get_password_hash("CustomerPass123!"),
            full_name="Rahul Sharma",
            role=UserRole.CUSTOMER.value,
            is_active=True
        )
        session.add(admin_user)
        session.add(customer_user)
        await session.flush()

        print("Seeding Categories...")
        # 2. Categories
        categories_data = [
            {"name": "Starters & Appetizers", "slug": "starters", "description": "Crispy, tandoori, and flavorful quick bites", "display_order": 1},
            {"name": "Main Course", "slug": "main-course", "description": "Authentic North & South Indian rich curries and gravies", "display_order": 2},
            {"name": "Biryani & Rice", "slug": "biryani", "description": "Slow-cooked dum biryanis and aromatic rice preparations", "display_order": 3},
            {"name": "South Indian Delicacies", "slug": "south-indian", "description": "Steamed and crispy traditional South Indian delights", "display_order": 4},
            {"name": "Healthy, Bowls & Salads", "slug": "healthy-bowls", "description": "Nutrient-dense, high-protein, and calorie-conscious meals", "display_order": 5},
            {"name": "Beverages", "slug": "beverages", "description": "Refreshing coolers, mocktails, and traditional shakes", "display_order": 6},
            {"name": "Desserts", "slug": "desserts", "description": "Traditional Indian sweets and guilt-free desserts", "display_order": 7},
        ]

        categories_map = {}
        for cat_info in categories_data:
            cat = Category(
                name=cat_info["name"],
                slug=cat_info["slug"],
                description=cat_info["description"],
                display_order=cat_info["display_order"],
                is_active=True
            )
            session.add(cat)
            await session.flush()
            categories_map[cat.slug] = cat.id

        print("Seeding Menu Items...")
        # 3. Rich Menu Dataset (26 Items specifically calibrated for NLP queries)
        menu_items_data = [
            # Starters
            {
                "category_slug": "starters",
                "name": "Paneer Tikka (Tandoori)",
                "description": "Cottage cheese cubes marinated in spiced yogurt and grilled in traditional clay oven.",
                "price": 190.0,
                "is_vegetarian": True,
                "is_spicy": True,
                "dietary_tags": ["high-protein", "gluten-free", "tandoor", "starter"],
                "popularity_score": 92.0,
                "is_available": True
            },
            {
                "category_slug": "starters",
                "name": "Chilli Paneer Dry",
                "description": "Crisp paneer cubes tossed in spicy green chillies, garlic, and tangy Indo-Chinese sauce.",
                "price": 180.0,
                "is_vegetarian": True,
                "is_spicy": True,
                "dietary_tags": ["spicy", "indo-chinese", "starter"],
                "popularity_score": 85.0,
                "is_available": True
            },
            {
                "category_slug": "starters",
                "name": "Crispy Golden Baby Corn",
                "description": "Crunchy golden fried baby corn dusted with peri-peri herbs and sea salt.",
                "price": 160.0,
                "is_vegetarian": True,
                "is_spicy": False,
                "dietary_tags": ["fried", "snack", "starter"],
                "popularity_score": 68.0,
                "is_available": True
            },
            {
                "category_slug": "starters",
                "name": "Steamed Veg Dimsums (6 pcs)",
                "description": "Delicate steamed dumplings stuffed with crunchy vegetables and ginger, served with spicy dip.",
                "price": 170.0,
                "is_vegetarian": True,
                "is_spicy": False,
                "dietary_tags": ["light", "non-fried", "low-calorie", "healthy", "starter"],
                "popularity_score": 88.0,
                "is_available": True
            },
            {
                "category_slug": "starters",
                "name": "Chicken Tikka Kebab",
                "description": "Tender boneless chicken marinated in red chili yogurt and roasted to perfection.",
                "price": 260.0,
                "is_vegetarian": False,
                "is_spicy": True,
                "dietary_tags": ["high-protein", "gluten-free", "tandoor", "starter"],
                "popularity_score": 95.0,
                "is_available": True
            },
            {
                "category_slug": "starters",
                "name": "Chicken 65 Classic",
                "description": "Fiery deep-fried chicken tossed with curry leaves, crushed pepper, and southern spices.",
                "price": 230.0,
                "is_vegetarian": False,
                "is_spicy": True,
                "dietary_tags": ["spicy", "high-protein", "fried", "regional", "starter"],
                "popularity_score": 90.0,
                "is_available": True
            },

            # Main Course
            {
                "category_slug": "main-course",
                "name": "Paneer Butter Masala",
                "description": "Rich cottage cheese cooked in creamy tomato butter gravy with aromatic kasuri methi.",
                "price": 260.0,
                "is_vegetarian": True,
                "is_spicy": False,
                "dietary_tags": ["rich", "creamy", "gravy", "classic", "main-course"],
                "popularity_score": 98.0,
                "is_available": True
            },
            {
                "category_slug": "main-course",
                "name": "Homestyle Dal Tadka",
                "description": "Yellow lentils tempered with cumin, garlic, tomatoes, and green chillies. Light and comforting.",
                "price": 150.0,
                "is_vegetarian": True,
                "is_spicy": True,
                "dietary_tags": ["light", "dairy-free", "vegan", "comfort-food", "healthy", "main-course"],
                "popularity_score": 94.0,
                "is_available": True
            },
            {
                "category_slug": "main-course",
                "name": "Pindi Chana Masala",
                "description": "Authentic chickpeas cooked in dry roasted Punjabi spices and ginger. 100% dairy-free.",
                "price": 180.0,
                "is_vegetarian": True,
                "is_spicy": True,
                "dietary_tags": ["vegan", "dairy-free", "high-fiber", "high-protein", "main-course"],
                "popularity_score": 82.0,
                "is_available": True
            },
            {
                "category_slug": "main-course",
                "name": "Soya Chaap Tikka Masala",
                "description": "High-protein plant soya chunks grilled and tossed in thick onion-tomato spicy masala.",
                "price": 210.0,
                "is_vegetarian": True,
                "is_spicy": True,
                "dietary_tags": ["high-protein", "vegetarian", "spicy", "main-course"],
                "popularity_score": 79.0,
                "is_available": True
            },
            {
                "category_slug": "main-course",
                "name": "Andhra Spicy Chicken Curry",
                "description": "Fiery country chicken simmered in ground Guntur red chillies and coconut paste.",
                "price": 290.0,
                "is_vegetarian": False,
                "is_spicy": True,
                "dietary_tags": ["spicy", "high-protein", "regional", "main-course"],
                "popularity_score": 91.0,
                "is_available": True
            },
            {
                "category_slug": "main-course",
                "name": "Butter Chicken Delhi Style",
                "description": "Succulent tandoori chicken cooked in silky smooth buttery makhani gravy.",
                "price": 310.0,
                "is_vegetarian": False,
                "is_spicy": False,
                "dietary_tags": ["rich", "creamy", "high-protein", "classic", "main-course"],
                "popularity_score": 99.0,
                "is_available": True
            },

            # Biryani
            {
                "category_slug": "biryani",
                "name": "Hyderabadi Chicken Dum Biryani",
                "description": "Fragrant basmati rice layered with spiced marinated chicken, saffron, and fried onions.",
                "price": 280.0,
                "is_vegetarian": False,
                "is_spicy": True,
                "dietary_tags": ["filling", "high-protein", "classic", "biryani"],
                "popularity_score": 100.0,
                "is_available": True
            },
            {
                "category_slug": "biryani",
                "name": "Vegetable Dum Biryani",
                "description": "Aromatic basmati rice cooked on slow flame with garden fresh vegetables and spices.",
                "price": 210.0,
                "is_vegetarian": True,
                "is_spicy": True,
                "dietary_tags": ["filling", "vegetarian", "aromatic", "biryani"],
                "popularity_score": 86.0,
                "is_available": True
            },

            # South Indian
            {
                "category_slug": "south-indian",
                "name": "Steamed Idli Sambar (4 pcs)",
                "description": "Fluffy steamed rice-lentil cakes served with steaming hot vegetable sambar and coconut chutney.",
                "price": 110.0,
                "is_vegetarian": True,
                "is_spicy": False,
                "dietary_tags": ["light", "non-fried", "healthy", "vegan", "breakfast", "lunch"],
                "popularity_score": 93.0,
                "is_available": True
            },
            {
                "category_slug": "south-indian",
                "name": "Ghee Podi Masala Dosa",
                "description": "Golden crispy fermented crepe smeared with aromatic spicy podi and filled with potato masala.",
                "price": 140.0,
                "is_vegetarian": True,
                "is_spicy": True,
                "dietary_tags": ["crispy", "classic", "south-indian"],
                "popularity_score": 96.0,
                "is_available": True
            },

            # Healthy & Bowls
            {
                "category_slug": "healthy-bowls",
                "name": "Grilled Herb Chicken Salad",
                "description": "Juicy grilled chicken strips on a bed of crisp greens, cherry tomatoes, and olive oil lemon dressing.",
                "price": 250.0,
                "is_vegetarian": False,
                "is_spicy": False,
                "dietary_tags": ["healthy", "high-protein", "non-fried", "low-carb", "light", "lunch"],
                "popularity_score": 89.0,
                "is_available": True
            },
            {
                "category_slug": "healthy-bowls",
                "name": "Sprouted Moong & Paneer Bowl",
                "description": "Protein-packed sprouted green moong tossed with fresh paneer, cucumber, lime, and chaat masala.",
                "price": 140.0,
                "is_vegetarian": True,
                "is_spicy": False,
                "dietary_tags": ["healthy", "high-protein", "non-fried", "light", "vegetarian", "lunch"],
                "popularity_score": 84.0,
                "is_available": True
            },
            {
                "category_slug": "healthy-bowls",
                "name": "Grilled Fish Fillet with Steamed Veggies",
                "description": "Fresh river fish marinated in lemon pepper and grilled, served with steamed broccoli and carrots.",
                "price": 320.0,
                "is_vegetarian": False,
                "is_spicy": False,
                "dietary_tags": ["high-protein", "non-fried", "healthy", "keto", "light"],
                "popularity_score": 75.0,
                "is_available": True
            },

            # Beverages
            {
                "category_slug": "beverages",
                "name": "Fresh Mint Lime Soda",
                "description": "Zesty squeezed lemon with crushed garden mint and sparkling soda. Available sweet or salted.",
                "price": 70.0,
                "is_vegetarian": True,
                "is_spicy": False,
                "dietary_tags": ["beverage", "light", "vegan", "dairy-free", "refreshing"],
                "popularity_score": 91.0,
                "is_available": True
            },
            {
                "category_slug": "beverages",
                "name": "Alphonso Mango Lassi",
                "description": "Thick sweetened yogurt blended with pure Alphonso mango pulp and cardamom.",
                "price": 110.0,
                "is_vegetarian": True,
                "is_spicy": False,
                "dietary_tags": ["beverage", "dairy", "sweet"],
                "popularity_score": 95.0,
                "is_available": True
            },
            {
                "category_slug": "beverages",
                "name": "Artisanal Cold Brew Coffee",
                "description": "Steeped for 18 hours in cold filtered water. Smooth, zero-bitterness energy boost.",
                "price": 130.0,
                "is_vegetarian": True,
                "is_spicy": False,
                "dietary_tags": ["beverage", "dairy-free", "vegan", "sugar-free"],
                "popularity_score": 78.0,
                "is_available": True
            },

            # Desserts
            {
                "category_slug": "desserts",
                "name": "Hot Gulab Jamun (2 pcs)",
                "description": "Warm golden milk-solid dumplings soaked in rose and saffron infused sugar syrup.",
                "price": 90.0,
                "is_vegetarian": True,
                "is_spicy": False,
                "dietary_tags": ["dessert", "sweet", "classic"],
                "popularity_score": 97.0,
                "is_available": True
            },
            {
                "category_slug": "desserts",
                "name": "Kesar Rasmalai (2 pcs)",
                "description": "Soft cottage cheese patties immersed in chilled saffron-pistachio clotted milk.",
                "price": 120.0,
                "is_vegetarian": True,
                "is_spicy": False,
                "dietary_tags": ["dessert", "sweet", "dairy"],
                "popularity_score": 92.0,
                "is_available": True
            },
            {
                "category_slug": "desserts",
                "name": "Sugar-free Coconut Chia Pudding",
                "description": "Chia seeds soaked in creamy coconut milk topped with toasted almond flakes and berries.",
                "price": 150.0,
                "is_vegetarian": True,
                "is_spicy": False,
                "dietary_tags": ["dessert", "healthy", "vegan", "dairy-free", "sugar-free"],
                "popularity_score": 73.0,
                "is_available": True
            },
            {
                "category_slug": "starters",
                "name": "Seasonal Special Fish Amritsari (Unavailable)",
                "description": "Carom-seed spiced crispy fish fillets. (Currently out of season).",
                "price": 280.0,
                "is_vegetarian": False,
                "is_spicy": True,
                "dietary_tags": ["starter", "seafood", "fried"],
                "popularity_score": 50.0,
                "is_available": False  # Tested for availability filter exclusion!
            }
        ]

        created_items = []
        for item_info in menu_items_data:
            cat_id = categories_map[item_info["category_slug"]]
            menu_item = MenuItem(
                category_id=cat_id,
                name=item_info["name"],
                description=item_info["description"],
                price=item_info["price"],
                is_vegetarian=item_info["is_vegetarian"],
                is_spicy=item_info["is_spicy"],
                dietary_tags=item_info["dietary_tags"],
                popularity_score=item_info["popularity_score"],
                is_available=item_info["is_available"]
            )
            session.add(menu_item)
            created_items.append(menu_item)

        await session.flush()

        print("Seeding Initial Sample Orders for Admin Dashboard...")
        # 4. Realistic Sample Orders
        now = datetime.now(timezone.utc)
        
        # Order 1: Completed Order earlier today
        order1 = Order(
            customer_id=customer_user.id,
            status=OrderStatus.PICKED_UP.value,
            total_amount=470.0,
            delivery_notes="Please ring doorbell",
            created_at=now - timedelta(hours=3)
        )
        session.add(order1)
        await session.flush()
        session.add(OrderItem(order_id=order1.id, menu_item_id=created_items[0].id, quantity=1, unit_price=190.0, subtotal=190.0))
        session.add(OrderItem(order_id=order1.id, menu_item_id=created_items[12].id, quantity=1, unit_price=280.0, subtotal=280.0))

        # Order 2: In-Kitchen Preparing Order
        order2 = Order(
            customer_id=customer_user.id,
            status=OrderStatus.PREPARING.value,
            total_amount=360.0,
            delivery_notes="Keep it spicy",
            created_at=now - timedelta(minutes=25)
        )
        session.add(order2)
        await session.flush()
        session.add(OrderItem(order_id=order2.id, menu_item_id=created_items[1].id, quantity=1, unit_price=180.0, subtotal=180.0))
        session.add(OrderItem(order_id=order2.id, menu_item_id=created_items[8].id, quantity=1, unit_price=180.0, subtotal=180.0))

        # Order 3: Newly Placed Order
        order3 = Order(
            customer_id=customer_user.id,
            status=OrderStatus.PLACED.value,
            total_amount=200.0,
            delivery_notes="Leave at front desk",
            created_at=now - timedelta(minutes=5)
        )
        session.add(order3)
        await session.flush()
        session.add(OrderItem(order_id=order3.id, menu_item_id=created_items[14].id, quantity=1, unit_price=110.0, subtotal=110.0))
        session.add(OrderItem(order_id=order3.id, menu_item_id=created_items[22].id, quantity=1, unit_price=90.0, subtotal=90.0))

        await session.commit()
        print("Database seeded successfully with users, categories, 26 menu items, and initial orders!")


if __name__ == "__main__":
    asyncio.run(seed_data())
