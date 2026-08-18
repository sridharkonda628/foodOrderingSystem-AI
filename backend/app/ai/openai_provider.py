import json
import logging
from typing import List, Optional
import openai
from app.ai.base import AIProvider
from app.core.config import settings
from app.schemas.search import SearchIntent

logger = logging.getLogger("kpitech_food_order")


class OpenAIProvider(AIProvider):
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.model = model or settings.OPENAI_MODEL
        self.client = openai.AsyncOpenAI(api_key=self.api_key) if self.api_key else None

    async def extract_intent(self, query: str) -> SearchIntent:
        if not self.client:
            raise ValueError("OpenAI client is not configured with a valid API key.")

        prompt = f"""Analyze the following user food search query and extract structured search constraints in JSON format.
Query: "{query}"

Return a JSON object with these exact keys:
{{
  "vegetarian": true | false | null,
  "spicy": true | false | null,
  "max_price": number | null,
  "min_price": number | null,
  "category": string | null,
  "preferred_tags": string[],
  "avoid_tags": string[],
  "meal_type": string | null,
  "extracted_keywords": string[]
}}

Notes:
- If user mentions "chicken", "meat", "fish", "mutton", "non-veg", vegetarian must be false.
- If user mentions "veg", "vegetarian", "paneer", vegetarian must be true.
- If user says "under 200" or "below 300", max_price must be that number.
- For tags like "high protein", "light", "non-fried", "dairy-free", add to preferred_tags.
- If user says "not fried", add "fried" to avoid_tags and "non-fried" to preferred_tags.
"""

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a specialized food search intent parser. Return valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.0,
            timeout=settings.AI_TIMEOUT_SECONDS
        )

        content = response.choices[0].message.content
        data = json.loads(content)
        return SearchIntent(**data)

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
        # Fast local fallback for explanation to avoid extra roundtrip latency
        tags_str = ", ".join(dietary_tags[:3]) if dietary_tags else ""
        veg_str = "Vegetarian" if is_vegetarian else "Non-veg"
        spicy_str = "spicy" if is_spicy else "mild"
        return f"{veg_str} ({spicy_str}) dish at ₹{price:.0f}. Matches '{query}' ({tags_str})."
