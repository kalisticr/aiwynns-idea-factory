"""
Similarity module for finding duplicate or similar concepts
"""

from typing import List, Tuple, Dict
from rapidfuzz import fuzz


class SimilarityFinder:
    """Find similar concepts across batches"""

    def __init__(self, database):
        self.db = database

    def find_similar_concepts(
        self,
        threshold: float = 0.8
    ) -> List[Tuple[Dict, Dict, float]]:
        """
        Find similar concepts across all batches

        Args:
            threshold: Similarity threshold (0.0 to 1.0)

        Returns:
            List of tuples: (concept1, concept2, similarity_score)
        """
        similar_pairs = []
        all_concepts = []

        # Gather all concepts from all batches
        for batch in self.db.get_all_batches():
            batch_id = batch.get('batch_id')
            for concept in batch.get('concepts', []):
                all_concepts.append({
                    'batch': batch_id,
                    'number': concept.get('number'),
                    'title': concept.get('title', ''),
                    'content': concept.get('content', ''),
                    'text': f"{concept.get('title', '')} {concept.get('content', '')}"
                })

        # Compare all pairs
        for i, concept1 in enumerate(all_concepts):
            for concept2 in all_concepts[i + 1:]:
                # Skip if from same batch
                if concept1['batch'] == concept2['batch']:
                    continue

                # Calculate similarity
                score = self._calculate_similarity(
                    concept1['text'],
                    concept2['text']
                )

                if score >= threshold:
                    similar_pairs.append((concept1, concept2, score))

        # Sort by similarity score (descending)
        similar_pairs.sort(key=lambda x: x[2], reverse=True)

        return similar_pairs

    def find_similar_to_concept(
        self,
        concept_text: str,
        limit: int = 10,
        threshold: float = 0.6
    ) -> List[Tuple[Dict, float]]:
        """
        Find concepts similar to a given text

        Args:
            concept_text: Text to compare against
            limit: Maximum number of results
            threshold: Minimum similarity threshold

        Returns:
            List of tuples: (concept, similarity_score)
        """
        results = []
        all_concepts = []

        # Gather all concepts
        for batch in self.db.get_all_batches():
            batch_id = batch.get('batch_id')
            for concept in batch.get('concepts', []):
                all_concepts.append({
                    'batch': batch_id,
                    'number': concept.get('number'),
                    'title': concept.get('title', ''),
                    'content': concept.get('content', ''),
                    'text': f"{concept.get('title', '')} {concept.get('content', '')}"
                })

        # Compare against all concepts
        for concept in all_concepts:
            score = self._calculate_similarity(concept_text, concept['text'])

            if score >= threshold:
                results.append((concept, score))

        # Sort by score and limit
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:limit]

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity between two texts

        Uses a combination of token set ratio and partial ratio
        for more robust similarity detection
        """
        # Token set ratio (good for unordered text)
        token_score = fuzz.token_set_ratio(text1.lower(), text2.lower())

        # Partial ratio (good for substring matches)
        partial_score = fuzz.partial_ratio(text1.lower(), text2.lower())

        # Weighted average
        combined_score = (token_score * 0.7 + partial_score * 0.3)

        return combined_score / 100.0

    def find_duplicate_titles(self) -> List[Tuple[str, List[str]]]:
        """
        Find concepts with duplicate or very similar titles

        Returns:
            List of tuples: (title, [batch_ids])
        """
        titles = {}

        for batch in self.db.get_all_batches():
            batch_id = batch.get('batch_id')
            for concept in batch.get('concepts', []):
                title = concept.get('title', '').strip().lower()
                if title:
                    if title not in titles:
                        titles[title] = []
                    titles[title].append(batch_id)

        # Return only titles that appear in multiple batches
        duplicates = [(title, batches) for title, batches in titles.items() if len(batches) > 1]
        duplicates.sort(key=lambda x: len(x[1]), reverse=True)

        return duplicates
