"""
Statistics and analytics module
"""

from collections import Counter
from typing import Dict, List


class StatsGenerator:
    """Generate statistics and analytics from the database"""

    def __init__(self, database):
        self.db = database

    def generate_stats(self) -> Dict:
        """Generate comprehensive statistics"""
        batches = self.db.get_all_batches()
        stories = self.db.get_all_stories()

        stats = {
            'total_batches': len(batches),
            'total_concepts': 0,
            'total_stories': len(stories),
            'stories_in_development': 0,
            'batches_by_status': Counter(),
            'genres': Counter(),
            'tropes': Counter(),
            'top_genres': [],
            'top_tropes': [],
            'recent_batches': []
        }

        # Analyze batches
        for batch in batches:
            stats['total_concepts'] += batch.get('count', 0)
            stats['batches_by_status'][batch.get('status', 'unknown')] += 1

            # Count genres
            genre = batch.get('genre', 'Unknown')
            if isinstance(genre, list):
                for g in genre:
                    stats['genres'][g] += 1
            else:
                stats['genres'][genre] += 1

            # Count tropes
            tropes = batch.get('tropes', [])
            if isinstance(tropes, str):
                # Parse comma-separated tropes
                tropes = [t.strip() for t in tropes.split(',')]
            if isinstance(tropes, list):
                for trope in tropes:
                    if trope:
                        stats['tropes'][trope] += 1

        # Analyze stories
        for story in stories:
            if story.get('status') == 'developing':
                stats['stories_in_development'] += 1

            # Count genres from stories
            genre = story.get('genre', 'Unknown')
            if isinstance(genre, list):
                for g in genre:
                    stats['genres'][g] += 1
            else:
                stats['genres'][genre] += 1

            # Count tropes from stories
            tropes = story.get('tropes', [])
            if isinstance(tropes, str):
                tropes = [t.strip() for t in tropes.split(',')]
            if isinstance(tropes, list):
                for trope in tropes:
                    if trope:
                        stats['tropes'][trope] += 1

        # Get top genres and tropes
        stats['top_genres'] = stats['genres'].most_common(10)
        stats['top_tropes'] = stats['tropes'].most_common(10)

        # Recent batches (sorted by date)
        stats['recent_batches'] = sorted(
            batches,
            key=lambda x: x.get('date_generated', ''),
            reverse=True
        )[:10]

        return stats

    def get_genre_breakdown(self) -> Dict[str, int]:
        """Get breakdown of all genres"""
        batches = self.db.get_all_batches()
        stories = self.db.get_all_stories()

        genres = Counter()

        for batch in batches:
            genre = batch.get('genre', 'Unknown')
            if isinstance(genre, list):
                for g in genre:
                    genres[g] += 1
            else:
                genres[genre] += 1

        for story in stories:
            genre = story.get('genre', 'Unknown')
            if isinstance(genre, list):
                for g in genre:
                    genres[g] += 1
            else:
                genres[genre] += 1

        return dict(genres)

    def get_trope_breakdown(self) -> Dict[str, int]:
        """Get breakdown of all tropes"""
        batches = self.db.get_all_batches()
        stories = self.db.get_all_stories()

        tropes = Counter()

        for batch in batches:
            batch_tropes = batch.get('tropes', [])
            if isinstance(batch_tropes, str):
                batch_tropes = [t.strip() for t in batch_tropes.split(',')]
            if isinstance(batch_tropes, list):
                for trope in batch_tropes:
                    if trope:
                        tropes[trope] += 1

        for story in stories:
            story_tropes = story.get('tropes', [])
            if isinstance(story_tropes, str):
                story_tropes = [t.strip() for t in story_tropes.split(',')]
            if isinstance(story_tropes, list):
                for trope in story_tropes:
                    if trope:
                        tropes[trope] += 1

        return dict(tropes)
