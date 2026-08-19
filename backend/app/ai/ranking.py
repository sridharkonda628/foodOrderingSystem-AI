"""
Hybrid Multi-Signal Relevance Scoring and Ranking Engine.

Use Case:
- Combines multiple relevance signals into a final normalized score (0.0 to 1.0) for menu items:
  1. Semantic Similarity: Jaccard token overlap between query and dish attributes with name match boost.
  2. Keyword Score: Ratio of extracted query keywords found in dish name/description/tags.
  3. Preference Score: Rewards preferred tags and applies penalties for avoided tags (e.g. "not fried").
  4. Popularity Score: Incorporates historical popularity / customer ratings.
"""

import re
from typing import List, Dict, Any, Tuple
from app.core.config import settings
from app.models.menu_item import MenuItem
from app.schemas.search import SearchIntent


class HybridRankingEngine:
    """
    Multi-signal relevance scoring engine.

    Formula:
    Final Score = (
        SEMANTIC_WEIGHT * semantic_score +
        KEYWORD_WEIGHT * keyword_score +
        PREFERENCE_WEIGHT * preference_score +
        POPULARITY_WEIGHT * popularity_score
    )
    """

    @staticmethod
    def _tokenize(text: str) -> set:
        """
        Tokenizes text into a set of normalized lowercase alphanumeric words of length >= 2.

        Parameters:
        - text: Input text string.

        Returns:
        - Set of word tokens.
        """
        tokens = re.findall(r"\b[a-z0-9]{2,}\b", text.lower())
        return set(tokens)

    @classmethod
    def calculate_keyword_score(cls, query_keywords: List[str], item: MenuItem) -> float:
        """
        Calculates the keyword match ratio between query keywords and dish properties.

        Use Case:
        - Evaluates presence of core food terms (e.g. "biryani", "paneer", "tikka") in dish title/description.

        Parameters:
        - query_keywords: List of extracted keywords from intent parser.
        - item: MenuItem entity to score.

        Returns:
        - Float score between 0.0 and 1.0.
        """
        if not query_keywords:
            return 0.5  # Neutral baseline if no specific keywords extracted

        target_text = f"{item.name} {item.description} {' '.join(item.dietary_tags)} {item.category.name if item.category else ''}"
        target_tokens = cls._tokenize(target_text)
        
        matches = sum(1 for kw in query_keywords if kw.lower() in target_tokens or any(kw.lower() in t for t in target_tokens))
        return min(1.0, matches / max(1, len(query_keywords)))

    @classmethod
    def calculate_semantic_score(cls, query: str, item: MenuItem) -> float:
        """
        Calculates Jaccard token similarity with a bonus for direct substring matches.

        Use Case:
        - Measures how closely the overall natural language prompt aligns with the dish's text.

        Parameters:
        - query: Raw query string.
        - item: MenuItem entity to score.

        Returns:
        - Float score between 0.0 and 1.0.
        """
        query_tokens = cls._tokenize(query)
        target_tokens = cls._tokenize(f"{item.name} {item.description} {' '.join(item.dietary_tags)}")
        
        if not query_tokens or not target_tokens:
            return 0.3

        # Jaccard Token Similarity
        intersection = query_tokens.intersection(target_tokens)
        union = query_tokens.union(target_tokens)
        jaccard = len(intersection) / len(union) if union else 0.0

        # Direct name substring match gives high semantic affinity
        name_boost = 0.4 if item.name.lower() in query.lower() or query.lower() in item.name.lower() else 0.0
        
        return min(1.0, (jaccard * 1.5) + name_boost)

    @classmethod
    def calculate_preference_score(cls, intent: SearchIntent, item: MenuItem) -> float:
        """
        Adjusts score based on preferred tags (bonuses) and avoided tags (penalties).

        Use Case:
        - Accurately penalizes dishes with "fried" tags when user requests "non-fried",
          and boosts items with "high-protein" or "light" tags when requested.

        Parameters:
        - intent: SearchIntent containing preferred_tags and avoid_tags.
        - item: MenuItem entity to score.

        Returns:
        - Float score clamped between 0.0 and 1.0.
        """
        score = 0.5  # Baseline

        # Avoid tags penalty (e.g. avoid 'fried' if user asked for 'non-fried')
        for avoid in intent.avoid_tags:
            if avoid.lower() in item.dietary_tags or avoid.lower() in item.name.lower() or avoid.lower() in item.description.lower():
                score -= 0.4

        # Preferred tags reward (e.g. bonus for 'high-protein', 'dairy-free')
        for pref in intent.preferred_tags:
            if pref.lower() in item.dietary_tags or pref.lower() in item.name.lower() or pref.lower() in item.description.lower():
                score += 0.3

        # Meal type reward
        if intent.meal_type and item.category:
            if intent.meal_type.lower() in item.category.slug.lower() or intent.meal_type.lower() in item.dietary_tags:
                score += 0.2

        return max(0.0, min(1.0, score))

    @classmethod
    def calculate_popularity_score(cls, item: MenuItem) -> float:
        """
        Normalizes dish popularity score (0 - 100) to a 0.0 - 1.0 factor.

        Parameters:
        - item: MenuItem entity.

        Returns:
        - Float score between 0.0 and 1.0.
        """
        return min(1.0, max(0.0, (item.popularity_score or 0.0) / 100.0))

    @classmethod
    def rank_items(
        cls,
        query: str,
        intent: SearchIntent,
        items: List[MenuItem]
    ) -> List[Tuple[MenuItem, float, List[str]]]:
        """
        Scores, annotates, and sorts a list of candidate dishes in descending order of relevance.

        Use Case:
        - Called by `MenuSearchService` to generate the final ordered recommendation list.

        Parameters:
        - query: Raw search query string.
        - intent: SearchIntent object with structured constraints and preferences.
        - items: List of candidate MenuItem entities.

        Returns:
        - List of Tuples: (MenuItem, final_relevance_score, list_of_badge_highlights).
        """
        ranked = []
        for item in items:
            semantic = cls.calculate_semantic_score(query, item)
            keyword = cls.calculate_keyword_score(intent.extracted_keywords, item)
            preference = cls.calculate_preference_score(intent, item)
            popularity = cls.calculate_popularity_score(item)

            final_score = (
                settings.SEMANTIC_WEIGHT * semantic +
                settings.KEYWORD_WEIGHT * keyword +
                settings.PREFERENCE_WEIGHT * preference +
                settings.POPULARITY_WEIGHT * popularity
            )
            final_score = round(max(0.01, min(0.99, final_score)), 2)

            # Generate UI highlight badges for this item
            highlights = []
            if item.is_vegetarian:
                highlights.append("Vegetarian")
            if item.is_spicy:
                highlights.append("Spicy")
            for t in item.dietary_tags[:2]:
                highlights.append(t.replace("-", " ").capitalize())

            ranked.append((item, final_score, highlights))

        # Sort descending by calculated relevance score
        ranked.sort(key=lambda x: x[1], reverse=True)
        return ranked
