"""
Indexer module for updating INDEX.md
"""

from pathlib import Path
from datetime import datetime


class Indexer:
    """Update the INDEX.md database file"""

    def __init__(self, project_root: Path, database):
        self.project_root = Path(project_root)
        self.index_file = self.project_root / "INDEX.md"
        self.db = database

    def update_index(self):
        """Rebuild INDEX.md with current database state"""
        batches = self.db.get_all_batches()
        stories = self.db.get_all_stories()

        # Calculate statistics
        total_batches = len(batches)
        total_concepts = sum(batch.get('count', 0) for batch in batches)
        total_stories = len(stories)
        stories_developing = sum(
            1 for story in stories if story.get('status') == 'developing'
        )

        # Start building content
        content = f"""# Story Concepts Index

This file tracks all story concepts in the database. Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M")}

## Statistics
- Total Batches: {total_batches}
- Total Concepts: {total_concepts}
- Stories in Development: {stories_developing}
- Total Stories: {total_stories}

---

## Concept Batches

"""

        # Group batches by location
        batches_by_location = {}
        for batch in batches:
            location = batch.get('location', 'unknown')
            if location not in batches_by_location:
                batches_by_location[location] = []
            batches_by_location[location].append(batch)

        # Add batches organized by location
        for location in ['generated', 'developing', 'favorites']:
            if location in batches_by_location:
                content += f"### {location.upper()}\n\n"

                for batch in sorted(
                    batches_by_location[location],
                    key=lambda x: x.get('date_generated', ''),
                    reverse=True
                ):
                    batch_id = batch.get('batch_id', 'N/A')
                    genre = batch.get('genre', 'N/A')
                    date = batch.get('date_generated', 'N/A')
                    count = batch.get('count', 0)

                    # Get relative path
                    file_path = Path(batch.get('file_path', ''))
                    try:
                        relpath = file_path.relative_to(self.project_root)
                    except ValueError:
                        relpath = file_path

                    content += f"- **[{batch_id}]** {genre} ({count} concepts) - {date} - `{relpath}`\n"

                content += "\n"

        content += """---

## Stories in Development

"""

        # Add stories
        for story in sorted(stories, key=lambda x: x.get('date_created', ''), reverse=True):
            title = story.get('title', 'Untitled')
            genre = story.get('genre', 'N/A')
            status = story.get('status', 'N/A')
            tropes = story.get('tropes', [])

            if isinstance(tropes, list):
                tropes_str = ', '.join(tropes)
            else:
                tropes_str = str(tropes)

            # Get relative path
            file_path = Path(story.get('file_path', ''))
            try:
                relpath = file_path.relative_to(self.project_root)
            except ValueError:
                relpath = file_path

            content += f"""- **{title}** [{status}]
  - Genre: {genre}
  - Tropes: {tropes_str}
  - File: `{relpath}`

"""

        content += """---

## Manual Updates
You can manually add notes and cross-references below this line.

"""

        # Write the index file
        with open(self.index_file, 'w') as f:
            f.write(content)
