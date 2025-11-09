"""
Database module for reading and managing concept batches and stories
"""

from pathlib import Path
from typing import List, Dict, Optional
import frontmatter
import yaml


class ConceptDatabase:
    """Manages reading concept batches and stories from markdown files"""

    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        self.concepts_dir = self.project_root / "concepts"
        self.stories_dir = self.project_root / "stories"

    def get_all_batches(self) -> List[Dict]:
        """Get all concept batches from all subdirectories"""
        batches = []

        for subdir in ['generated', 'developing', 'favorites']:
            batch_dir = self.concepts_dir / subdir
            if batch_dir.exists():
                for md_file in batch_dir.glob("*.md"):
                    batch_data = self._parse_batch_file(md_file)
                    if batch_data:
                        batch_data['location'] = subdir
                        batches.append(batch_data)

        return batches

    def get_batch(self, batch_id: str) -> Optional[Dict]:
        """Get a specific batch by ID"""
        for batch in self.get_all_batches():
            if batch.get('batch_id') == batch_id:
                return batch
        return None

    def get_all_stories(self) -> List[Dict]:
        """Get all story development files"""
        stories = []

        if self.stories_dir.exists():
            for md_file in self.stories_dir.glob("*.md"):
                story_data = self._parse_story_file(md_file)
                if story_data:
                    stories.append(story_data)

        return stories

    def _parse_batch_file(self, file_path: Path) -> Optional[Dict]:
        """Parse a batch markdown file with frontmatter"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)

            metadata = dict(post.metadata)
            metadata['file_path'] = str(file_path)
            metadata['content'] = post.content

            # Extract concepts from content
            concepts = self._extract_concepts_from_content(post.content)
            metadata['concepts'] = concepts

            return metadata

        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return None

    def _parse_story_file(self, file_path: Path) -> Optional[Dict]:
        """Parse a story development markdown file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)

            metadata = dict(post.metadata)
            metadata['file_path'] = str(file_path)
            metadata['content'] = post.content

            return metadata

        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return None

    def _extract_concepts_from_content(self, content: str) -> List[Dict]:
        """Extract individual concepts from batch content"""
        concepts = []
        current_concept = None

        for line in content.split('\n'):
            # Look for concept headers (## Concept N:)
            if line.startswith('## Concept '):
                if current_concept:
                    concepts.append(current_concept)

                # Extract concept number and title
                parts = line.replace('## Concept ', '').split(':', 1)
                number = parts[0].strip()
                title = parts[1].strip() if len(parts) > 1 else ''

                current_concept = {
                    'number': number,
                    'title': title,
                    'content': ''
                }
            elif current_concept:
                current_concept['content'] += line + '\n'

        # Add last concept
        if current_concept:
            concepts.append(current_concept)

        return concepts

    def get_all_files(self) -> List[Path]:
        """Get all markdown files (batches and stories)"""
        files = []

        # Get concept batches
        for subdir in ['generated', 'developing', 'favorites']:
            batch_dir = self.concepts_dir / subdir
            if batch_dir.exists():
                files.extend(batch_dir.glob("*.md"))

        # Get stories
        if self.stories_dir.exists():
            files.extend(self.stories_dir.glob("*.md"))

        return files
