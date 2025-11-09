"""
Creator module for generating new batches and stories from templates
"""

from pathlib import Path
from datetime import datetime
import re
import logging
from .validation import (
    validate_string,
    validate_integer,
    validate_slug,
    ValidationError
)

logger = logging.getLogger(__name__)


class Creator:
    """Create new concept batches and story development files"""

    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        self.templates_dir = self.project_root / "templates"
        self.concepts_dir = self.project_root / "concepts" / "generated"
        self.stories_dir = self.project_root / "stories"

    def create_batch(
        self,
        genre: str,
        tropes: str,
        model: str,
        count: int = 10
    ) -> Path:
        """
        Create a new concept batch file from template

        Args:
            genre: Story genre
            tropes: Comma-separated tropes
            model: LLM model used
            count: Number of concepts in batch

        Returns:
            Path to created file

        Raises:
            ValidationError: If inputs are invalid
        """
        # Validate inputs
        genre = validate_string(genre, "genre", min_length=1, max_length=100)
        tropes = validate_string(tropes, "tropes", min_length=1, max_length=500)
        model = validate_string(model, "model", min_length=1, max_length=100)
        count = validate_integer(count, "count", min_value=1, max_value=50)

        logger.info(f"Creating batch: genre={genre}, count={count}")

        # Generate batch ID
        today = datetime.now().strftime("%Y%m%d")
        batch_num = 1

        while (self.concepts_dir / f"{today}-{batch_num:03d}.md").exists():
            batch_num += 1

        batch_id = f"{today}-{batch_num:03d}"
        new_file = self.concepts_dir / f"{batch_id}.md"
        logger.debug(f"Generated batch ID: {batch_id}")

        # Read template
        template_file = self.templates_dir / "concept-batch.md"
        logger.debug(f"Reading template: {template_file}")
        with open(template_file, 'r') as f:
            content = f.read()

        # Replace placeholders
        content = content.replace("YYYYMMDD-001", batch_id)
        content = content.replace("YYYY-MM-DD", datetime.now().strftime("%Y-%m-%d"))
        content = content.replace("[genre]", genre)
        content = content.replace("[trope1, trope2, trope3]", tropes)
        content = content.replace("count: 10", f"count: {count}")
        content = content.replace('"model used"', f'"{model}"')

        # Write file
        logger.debug(f"Writing batch file: {new_file}")
        with open(new_file, 'w') as f:
            f.write(content)

        logger.info(f"Created batch: {batch_id} at {new_file}")
        return new_file

    def create_story(
        self,
        title: str,
        genre: str,
        origin: str = None
    ) -> Path:
        """
        Create a new story development file from template

        Args:
            title: Story title
            genre: Story genre
            origin: Optional origin batch ID

        Returns:
            Path to created file

        Raises:
            ValidationError: If inputs are invalid
        """
        # Validate inputs
        title = validate_string(title, "title", min_length=1, max_length=200)
        genre = validate_string(genre, "genre", min_length=1, max_length=100)

        logger.info(f"Creating story: title='{title}', genre={genre}")

        # Create filename from title
        filename = self._slugify(title)

        # Validate the generated slug
        if not filename:
            logger.error(f"Title '{title}' produces empty filename after slugification")
            raise ValidationError(
                f"Title '{title}' produces an empty filename after slugification"
            )

        new_file = self.stories_dir / f"{filename}.md"

        # Check if file exists
        if new_file.exists():
            logger.warning(f"Story file already exists: {new_file}, adding timestamp")
            timestamp = datetime.now().strftime("%Y%m%d")
            new_file = self.stories_dir / f"{filename}-{timestamp}.md"

        # Generate story ID
        story_id = f"{filename}-{int(datetime.now().timestamp())}"
        logger.debug(f"Generated story ID: {story_id}")

        # Read template
        template_file = self.templates_dir / "story-development.md"
        logger.debug(f"Reading template: {template_file}")
        with open(template_file, 'r') as f:
            content = f.read()

        # Replace placeholders
        content = content.replace("[unique-id]", story_id)
        content = content.replace("[Working Title]", title)
        content = content.replace("[Story Title]", title)
        content = content.replace("[genre]", genre)
        content = content.replace(
            "[batch_id if from generated concepts]",
            origin if origin else "none"
        )
        content = content.replace("YYYY-MM-DD", datetime.now().strftime("%Y-%m-%d"))

        # Write file
        logger.debug(f"Writing story file: {new_file}")
        with open(new_file, 'w') as f:
            f.write(content)

        logger.info(f"Created story: {filename} at {new_file}")
        return new_file

    def _slugify(self, text: str) -> str:
        """Convert text to slug (lowercase, hyphens)"""
        # Convert to lowercase
        text = text.lower()
        # Replace spaces with hyphens
        text = text.replace(' ', '-')
        # Remove non-alphanumeric characters except hyphens
        text = re.sub(r'[^a-z0-9-]', '', text)
        # Remove multiple consecutive hyphens
        text = re.sub(r'-+', '-', text)
        # Strip hyphens from ends
        text = text.strip('-')
        return text
