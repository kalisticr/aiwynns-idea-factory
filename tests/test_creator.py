"""
Tests for creator.py - File generation
"""

import pytest
from pathlib import Path
from datetime import datetime
from aiwynns.creator import Creator


class TestCreator:
    """Test the Creator class"""

    def test_init(self, temp_workspace):
        """Test creator initialization"""
        creator = Creator(temp_workspace)

        assert creator.project_root == temp_workspace
        assert creator.templates_dir == temp_workspace / "templates"
        assert creator.concepts_dir == temp_workspace / "concepts" / "generated"
        assert creator.stories_dir == temp_workspace / "stories"

    def test_create_batch(self, temp_workspace, mock_templates):
        """Test creating a new batch file"""
        creator = Creator(temp_workspace)

        file_path = creator.create_batch(
            genre="Fantasy",
            tropes="magic, adventure",
            model="Claude Sonnet 4.5",
            count=10
        )

        # Check file was created
        assert file_path.exists()
        assert file_path.suffix == '.md'

        # Check content
        content = file_path.read_text()
        assert "genre: Fantasy" in content
        assert "tropes: magic, adventure" in content
        assert "Claude Sonnet 4.5" in content
        assert "count: 10" in content

    def test_create_batch_generates_sequential_ids(self, temp_workspace, mock_templates):
        """Test that batch IDs increment correctly"""
        creator = Creator(temp_workspace)

        # Create first batch
        file1 = creator.create_batch("Fantasy", "magic", "Test", 10)
        batch_id1 = file1.stem

        # Create second batch (same day)
        file2 = creator.create_batch("SciFi", "aliens", "Test", 10)
        batch_id2 = file2.stem

        # IDs should be sequential
        assert batch_id1.endswith('-001')
        assert batch_id2.endswith('-002')

    def test_create_story(self, temp_workspace, mock_templates):
        """Test creating a new story file"""
        creator = Creator(temp_workspace)

        file_path = creator.create_story(
            title="The Magic Sword",
            genre="Fantasy",
            origin="20250101-001"
        )

        # Check file was created
        assert file_path.exists()
        assert file_path.name == "the-magic-sword.md"

        # Check content
        content = file_path.read_text()
        assert "title: The Magic Sword" in content
        assert "genre: Fantasy" in content
        assert "origin_batch: 20250101-001" in content

    def test_create_story_duplicate_title(self, temp_workspace, mock_templates):
        """Test creating stories with duplicate titles"""
        creator = Creator(temp_workspace)

        # Create first story
        file1 = creator.create_story("Test Story", "Fantasy", None)

        # Create second story with same title
        file2 = creator.create_story("Test Story", "Fantasy", None)

        # Files should be different
        assert file1 != file2
        assert file1.exists()
        assert file2.exists()

        # Second file should have timestamp suffix
        today = datetime.now().strftime("%Y%m%d")
        assert today in file2.name

    def test_create_story_no_origin(self, temp_workspace, mock_templates):
        """Test creating a story without origin batch"""
        creator = Creator(temp_workspace)

        file_path = creator.create_story(
            title="Original Story",
            genre="Mystery"
        )

        content = file_path.read_text()
        assert "origin_batch: none" in content

    def test_slugify(self, temp_workspace):
        """Test the slug generation"""
        creator = Creator(temp_workspace)

        # Basic slugification
        assert creator._slugify("Hello World") == "hello-world"

        # Special characters removed
        assert creator._slugify("Test! Story?") == "test-story"

        # Multiple spaces become single hyphen
        assert creator._slugify("Multiple   Spaces") == "multiple-spaces"

        # Leading/trailing hyphens removed
        assert creator._slugify("  Test Story  ") == "test-story"

        # Numbers preserved
        assert creator._slugify("Story 123") == "story-123"

        # Apostrophes and quotes removed
        assert creator._slugify("John's Story") == "johns-story"

        # Multiple hyphens collapsed
        assert creator._slugify("Test---Story") == "test-story"

    def test_slugify_edge_cases(self, temp_workspace):
        """Test slug generation edge cases"""
        creator = Creator(temp_workspace)

        # Empty string after cleaning
        assert creator._slugify("!!!") == ""

        # Only spaces
        assert creator._slugify("   ") == ""

        # Unicode characters
        assert creator._slugify("Café Résumé") == "caf-rsum"

    def test_create_batch_template_missing(self, temp_workspace):
        """Test creating batch when template is missing"""
        from aiwynns.exceptions import TemplateNotFoundError

        creator = Creator(temp_workspace)

        with pytest.raises(TemplateNotFoundError) as exc_info:
            creator.create_batch("Fantasy", "magic", "Test", 10)

        # Verify error message is informative
        assert "concept-batch.md" in str(exc_info.value)
        assert "not found" in str(exc_info.value)

    def test_create_story_template_missing(self, temp_workspace):
        """Test creating story when template is missing"""
        from aiwynns.exceptions import TemplateNotFoundError

        creator = Creator(temp_workspace)

        with pytest.raises(TemplateNotFoundError) as exc_info:
            creator.create_story("Test", "Fantasy")

        # Verify error message is informative
        assert "story-development.md" in str(exc_info.value)
        assert "not found" in str(exc_info.value)

    def test_create_batch_with_special_characters(self, temp_workspace, mock_templates):
        """Test creating batch with special characters in metadata"""
        creator = Creator(temp_workspace)

        file_path = creator.create_batch(
            genre="Science Fiction & Fantasy",
            tropes="time travel, first contact, aliens",
            model='Claude "Sonnet" 4.5',
            count=5
        )

        content = file_path.read_text()
        assert "Science Fiction & Fantasy" in content
        assert "time travel, first contact, aliens" in content

    def test_batch_directory_created(self, tmp_path):
        """Test that batch directory is created if it doesn't exist"""
        workspace = tmp_path / "new_workspace"
        workspace.mkdir()
        (workspace / "templates").mkdir()

        # Create mock template
        template = workspace / "templates" / "concept-batch.md"
        template.write_text("---\nbatch_id: YYYYMMDD-001\n---\nContent")

        creator = Creator(workspace)

        # concepts/generated doesn't exist yet
        assert not creator.concepts_dir.exists()

        # Should create it automatically
        creator.concepts_dir.mkdir(parents=True, exist_ok=True)
        file_path = creator.create_batch("Test", "test", "Test", 1)

        assert file_path.exists()

    def test_story_directory_created(self, tmp_path):
        """Test that story directory is created if it doesn't exist"""
        workspace = tmp_path / "new_workspace"
        workspace.mkdir()
        (workspace / "templates").mkdir()

        # Create mock template
        template = workspace / "templates" / "story-development.md"
        template.write_text("---\nstory_id: [unique-id]\n---\nContent")

        creator = Creator(workspace)

        # stories doesn't exist yet
        assert not creator.stories_dir.exists()

        # Should create it automatically
        creator.stories_dir.mkdir(parents=True, exist_ok=True)
        file_path = creator.create_story("Test", "Test")

        assert file_path.exists()


class TestCreatorValidation:
    """Test validation in Creator methods"""

    def test_create_batch_invalid_genre(self, temp_workspace, mock_templates):
        """Test that empty genre raises ValidationError"""
        from aiwynns.validation import ValidationError

        creator = Creator(temp_workspace)

        with pytest.raises(ValidationError):
            creator.create_batch("", "magic", "Test", 10)

    def test_create_batch_invalid_count_negative(self, temp_workspace, mock_templates):
        """Test that negative count raises ValidationError"""
        from aiwynns.validation import ValidationError

        creator = Creator(temp_workspace)

        with pytest.raises(ValidationError):
            creator.create_batch("Fantasy", "magic", "Test", -5)

    def test_create_batch_invalid_count_too_large(self, temp_workspace, mock_templates):
        """Test that count > 50 raises ValidationError"""
        from aiwynns.validation import ValidationError

        creator = Creator(temp_workspace)

        with pytest.raises(ValidationError):
            creator.create_batch("Fantasy", "magic", "Test", 100)

    def test_create_story_invalid_title(self, temp_workspace, mock_templates):
        """Test that empty title raises ValidationError"""
        from aiwynns.validation import ValidationError

        creator = Creator(temp_workspace)

        with pytest.raises(ValidationError):
            creator.create_story("   ", "Fantasy")

    def test_create_story_invalid_slug_result(self, temp_workspace, mock_templates):
        """Test that title producing empty slug raises ValidationError"""
        from aiwynns.validation import ValidationError

        creator = Creator(temp_workspace)

        # Title with only special characters will produce empty slug
        with pytest.raises(ValidationError) as exc_info:
            creator.create_story("!!!", "Fantasy")

        assert "empty filename" in str(exc_info.value)


class TestSlugifySecurity:
    """Test slug generation for security issues"""

    def test_path_traversal_prevention(self, temp_workspace):
        """Test that path traversal attempts are neutralized"""
        creator = Creator(temp_workspace)

        # Attempts to traverse up directories
        assert ".." not in creator._slugify("../../../etc/passwd")
        assert "/" not in creator._slugify("../../test")
        assert "\\" not in creator._slugify("..\\..\\test")

    def test_null_byte_injection(self, temp_workspace):
        """Test that null bytes are removed"""
        creator = Creator(temp_workspace)

        result = creator._slugify("test\x00.md")
        assert "\x00" not in result

    def test_no_hidden_files(self, temp_workspace):
        """Test that hidden file patterns are handled"""
        creator = Creator(temp_workspace)

        # Leading dots should be removed by strip
        result = creator._slugify(".hidden")
        assert not result.startswith('.')
