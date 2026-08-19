"""
Abstract AI Provider Interface.

Use Case:
- Defines the common contract for AI and NLP providers (e.g. `OpenAIProvider`, `MockAIProvider`).
- Allows seamless switching between live LLM APIs and deterministic local NLP engines without code changes.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from app.schemas.search import SearchIntent


class AIProvider(ABC):
    """
    Abstract base class for all AI/NLP search intent providers.
    """

    @abstractmethod
    async def extract_intent(self, query: str) -> SearchIntent:
        """
        Extracts structured search intent from a raw natural language query string.

        Use Case:
        - Parses queries like "vegetarian high protein under 250" into structured boolean/numeric filters and tags.

        Parameters:
        - query: Raw search query string.

        Returns:
        - SearchIntent model instance.
        """
        pass

    @abstractmethod
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
        Generates a concise, user-friendly explanation of why a dish matched the customer's query.

        Use Case:
        - Displayed on the search result cards (e.g., "High protein, non-fried vegetarian dish at ₹190").

        Parameters:
        - query: The original search prompt.
        - item_name: Name of the dish.
        - item_desc: Description of the dish.
        - dietary_tags: List of dietary tags on the dish.
        - price: Unit price of the dish in INR.
        - is_vegetarian: Whether the dish is vegetarian.
        - is_spicy: Whether the dish is spicy.

        Returns:
        - Concise match explanation string.
        """
        pass
