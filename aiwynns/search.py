"""
Search module with fuzzy matching and advanced filtering
"""

from typing import List, Dict, Optional
import logging
from rapidfuzz import fuzz, process
from .validation import (
    sanitize_search_query,
    validate_limit,
    validate_string,
    ValidationError
)

logger = logging.getLogger(__name__)


class SearchEngine:
    """Advanced search with fuzzy matching"""

    def __init__(self, database):
        self.db = database

    def search(
        self,
        query: str,
        genre: Optional[str] = None,
        trope: Optional[str] = None,
        status: Optional[str] = None,
        fuzzy: bool = False,
        limit: int = 20
    ) -> List[Dict]:
        """
        Search through all concepts and stories

        Args:
            query: Search term
            genre: Filter by genre
            trope: Filter by trope
            status: Filter by status
            fuzzy: Use fuzzy string matching
            limit: Maximum results to return

        Raises:
            ValidationError: If inputs are invalid
        """
        # Validate inputs
        query = sanitize_search_query(query)
        limit = validate_limit(limit)

        # Validate optional filters
        if genre:
            genre = validate_string(genre, "genre", max_length=100)
        if trope:
            trope = validate_string(trope, "trope", max_length=100)
        if status:
            status = validate_string(status, "status", max_length=50)

        logger.info(f"Searching: query='{query}', fuzzy={fuzzy}, limit={limit}, genre={genre}, trope={trope}, status={status}")

        results = []

        # Search batches
        for batch in self.db.get_all_batches():
            # Apply filters
            if genre and genre.lower() not in str(batch.get('genre', '')).lower():
                continue
            if status and batch.get('status') != status:
                continue
            if trope and trope.lower() not in str(batch.get('tropes', '')).lower():
                continue

            # Search in batch metadata
            searchable = f"{batch.get('genre', '')} {batch.get('tropes', '')} {batch.get('notes', '')}"

            # Search in individual concepts
            for concept in batch.get('concepts', []):
                concept_text = f"{concept.get('title', '')} {concept.get('content', '')}"
                searchable += " " + concept_text

                if fuzzy:
                    score = fuzz.partial_ratio(query.lower(), concept_text.lower())
                    if score > 60:  # Threshold for fuzzy matching
                        results.append({
                            'type': 'concept',
                            'title': concept.get('title', 'Untitled'),
                            'batch_id': batch.get('batch_id'),
                            'genre': batch.get('genre'),
                            'file': batch.get('file_path'),
                            'score': score / 100.0,
                            'preview': concept_text[:200]
                        })
                else:
                    if query.lower() in concept_text.lower():
                        results.append({
                            'type': 'concept',
                            'title': concept.get('title', 'Untitled'),
                            'batch_id': batch.get('batch_id'),
                            'genre': batch.get('genre'),
                            'file': batch.get('file_path'),
                            'preview': self._get_preview(concept_text, query)
                        })

        # Search stories
        for story in self.db.get_all_stories():
            # Apply filters
            if genre and genre.lower() not in str(story.get('genre', '')).lower():
                continue
            if status and story.get('status') != status:
                continue
            if trope and trope.lower() not in str(story.get('tropes', '')).lower():
                continue

            story_text = f"{story.get('title', '')} {story.get('content', '')}"

            if fuzzy:
                score = fuzz.partial_ratio(query.lower(), story_text.lower())
                if score > 60:
                    results.append({
                        'type': 'story',
                        'title': story.get('title', 'Untitled'),
                        'genre': story.get('genre'),
                        'file': story.get('file_path'),
                        'score': score / 100.0,
                        'preview': story_text[:200]
                    })
            else:
                if query.lower() in story_text.lower():
                    results.append({
                        'type': 'story',
                        'title': story.get('title', 'Untitled'),
                        'genre': story.get('genre'),
                        'file': story.get('file_path'),
                        'preview': self._get_preview(story_text, query)
                    })

        # Sort results by score if fuzzy matching
        if fuzzy:
            results.sort(key=lambda x: x.get('score', 0), reverse=True)

        limited_results = results[:limit]
        logger.info(f"Search completed: found {len(results)} results, returning {len(limited_results)}")
        logger.debug(f"Result types: {[r['type'] for r in limited_results]}")

        return limited_results

    def _get_preview(self, text: str, query: str, context_chars: int = 100) -> str:
        """Get a preview of text around the query match"""
        query_lower = query.lower()
        text_lower = text.lower()

        idx = text_lower.find(query_lower)
        if idx == -1:
            return text[:200]

        start = max(0, idx - context_chars)
        end = min(len(text), idx + len(query) + context_chars)

        preview = text[start:end]
        if start > 0:
            preview = '...' + preview
        if end < len(text):
            preview = preview + '...'

        return preview
