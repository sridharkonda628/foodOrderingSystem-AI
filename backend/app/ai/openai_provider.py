"""
OpenAI LLM Intent Extraction Provider.

Use Case:
- Integrates with OpenAI's Chat Completions API using JSON structured output mode.
- Extracts complex, nuanced natural language intents from user prompts (e.g., handling slang, synonyms, complex negations).
"""

import json
import logging
from typing import List, Optional
import openai
from app.ai.base import AIProvider
from app.core.config import settings
from app.schemas.search import SearchIntent

logger = logging.getLogger("kpitech_food_order")


class OpenAIProvider(AIProvider):
    """
    OpenAI-backed Intent Extraction Provider.

    Use Case:
    - Sends structured prompts to OpenAI models (e.g. GPT-4o-mini) to parse search criteria with JSON mode.
    """

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initializes the async OpenAI client.

        Parameters:
        - api_key: Optional API key override (defaults to settings.OPENAI_API_KEY).
        - model: Optional model override (defaults to settings.OPENAI_MODEL).
        """
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.model = model or settings.OPENAI_MODEL
        self.client = openai.AsyncOpenAI(api_key=self.api_key) if self.api_key else None

    async def extract_intent(self, query: str) -> SearchIntent:
        """
        Calls OpenAI API with JSON schema instructions to extract structured search constraints.

        Use Case:
        - Handles complex natural language food prompts with LLM semantic reasoning.

        Parameters:
        - query: Raw search query string.

        Returns:
        - SearchIntent model parsed from JSON LLM output.

        Raises:
        - ValueError: If OpenAI client is unconfigured.
        - Exception: If OpenAI API request fails or times out (triggers fallback in search service).
        """
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
        """
        Generates a concise match explanation for search result cards.

        Use Case:
        - Uses fast local formatting to avoid unnecessary extra LLM roundtrips and minimize latency.

        Parameters:
        - query: Original user search query.
        - item_name: Name of the dish.
        - item_desc: Description of the dish.
        - dietary_tags: List of dietary tags.
        - price: Dish price.
        - is_vegetarian: Boolean veg flag.
        - is_spicy: Boolean spicy flag.

        Returns:
        - Concise match explanation string.
        """
        tags_str = ", ".join(dietary_tags[:3]) if dietary_tags else ""
        veg_str = "Vegetarian" if is_vegetarian else "Non-veg"
        spicy_str = "spicy" if is_spicy else "mild"
        return f"{veg_str} ({spicy_str}) dish at ₹{price:.0f}. Matches '{query}' ({tags_str})."
