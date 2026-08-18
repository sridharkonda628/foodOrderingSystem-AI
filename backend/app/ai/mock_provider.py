import re
from typing import List, Optional
from app.ai.base import AIProvider
from app.schemas.search import SearchIntent


class MockAIProvider(AIProvider):
    """
    Rule-based NLP Intent Extractor that mimics LLM structured output.
    Used for local testing, zero-cost development, and deterministic fallback.
    """
    async def extract_intent(self, query: str) -> SearchIntent:
        q = query.lower().strip()

        # 1. Price extraction (e.g. "under 200", "below 300", "< 150", "under ₹250")
        max_price: Optional[float] = None
        price_match = re.search(r"(?:under|below|less than|<|within|upto|up to)\s*(?:rs\.?|inr|₹)?\s*(\d+)", q)
        if price_match:
            max_price = float(price_match.group(1))
        elif "budget" in q or "cheap" in q or "affordable" in q:
            max_price = 200.0

        # 2. Vegetarian / Non-Vegetarian detection
        vegetarian: Optional[bool] = None
        if any(term in q for term in ["non-veg", "non veg", "chicken", "meat", "fish", "mutton", "egg"]):
            vegetarian = False
        elif any(term in q for term in ["veg", "vegetarian", "paneer", "dal", "vegan", "plant-based"]):
            vegetarian = True

        # 3. Spicy detection
        spicy: Optional[bool] = None
        if any(term in q for term in ["not spicy", "mild", "sweet", "non spicy", "non-spicy", "less spicy"]):
            spicy = False
        elif any(term in q for term in ["spicy", "hot", "tikka", "chilli", "chili", "pepper", "masala", "pungent"]):
            spicy = True

        # 4. Dietary preferences & avoid tags
        preferred_tags: List[str] = []
        avoid_tags: List[str] = []

        if "high protein" in q or "protein" in q or "gym" in q:
            preferred_tags.append("high-protein")
        
        if "light" in q or "low calorie" in q or "diet" in q or "healthy" in q:
            preferred_tags.append("light")
            preferred_tags.append("healthy")

        if "not fried" in q or "non-fried" in q or "non fried" in q or "no fried" in q or "steamed" in q or "baked" in q:
            preferred_tags.append("non-fried")
            avoid_tags.append("fried")

        if "without dairy" in q or "no dairy" in q or "dairy-free" in q or "dairy free" in q or "vegan" in q:
            preferred_tags.append("dairy-free")
            preferred_tags.append("vegan")
            avoid_tags.append("dairy")

        # 5. Meal type detection
        meal_type: Optional[str] = None
        if "breakfast" in q or "morning" in q:
            meal_type = "breakfast"
        elif "lunch" in q:
            meal_type = "lunch"
        elif "dinner" in q:
            meal_type = "dinner"
        elif "snack" in q or "starter" in q or "appetizer" in q:
            meal_type = "starter"
        elif "dessert" in q or "sweet" in q:
            meal_type = "dessert"
        elif "drink" in q or "beverage" in q or "juice" in q:
            meal_type = "beverage"

        # 6. Extract core search keywords (filter out stop words)
        stop_words = {
            "something", "a", "an", "the", "under", "below", "rupees", "rs", "inr", "for",
            "and", "with", "without", "that", "is", "not", "too", "give", "me", "find",
            "show", "want", "like", "food", "dish", "dishes", "item", "items", "please"
        }
        tokens = re.findall(r"[a-zA-Z]{3,}", q)
        extracted_keywords = [t for t in tokens if t not in stop_words]

        return SearchIntent(
            vegetarian=vegetarian,
            spicy=spicy,
            max_price=max_price,
            min_price=None,
            category=meal_type,
            preferred_tags=list(set(preferred_tags)),
            avoid_tags=list(set(avoid_tags)),
            meal_type=meal_type,
            extracted_keywords=extracted_keywords
        )

    async def generate_explanation(
        self,
        query: str,
        item_name: str,
        item_desc: str,
        dietary_tags: List[str],
        price: float,
        is_vegetarian: bool,
        is_spicy: bool
    ) -> str:
        reasons = []
        if is_vegetarian:
            reasons.append("Vegetarian")
        else:
            reasons.append("Non-Veg")

        if is_spicy:
            reasons.append("Spicy")

        if "high-protein" in dietary_tags:
            reasons.append("High protein")
        if "non-fried" in dietary_tags:
            reasons.append("Non-fried")
        if "light" in dietary_tags:
            reasons.append("Light meal")
        if "dairy-free" in dietary_tags:
            reasons.append("Dairy-free")

        joined_reasons = ", ".join(reasons) if reasons else "Good menu match"
        return f"{joined_reasons} at ₹{price:,.0f}"
