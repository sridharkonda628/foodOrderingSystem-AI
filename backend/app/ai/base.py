from abc import ABC, abstractmethod
from typing import List, Optional
from app.schemas.search import SearchIntent


class AIProvider(ABC):
    @abstractmethod
    async def extract_intent(self, query: str) -> SearchIntent:
        """
        Extract structured search intent from natural language query.
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
        Generate a concise, user-friendly explanation of why the item matched the query.
        """
        pass
