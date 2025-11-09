"""
Tests for database.py - Data access layer
"""

import pytest
from pathlib import Path
from aiwynns.database import ConceptDatabase


class TestConceptDatabase:
    """Test the ConceptDatabase class"""

    def test_init(self, temp_workspace):
        """Test database initialization"""
        db = ConceptDatabase(temp_workspace)

        assert db.project_root == temp_workspace
        assert db.concepts_dir == temp_workspace / "concepts"
        assert db.stories_dir == temp_workspace / "stories"

    def test_get_all_batches_empty(self, temp_workspace):
        """Test getting batches from empty directory"""
        db = ConceptDatabase(temp_workspace)
        batches = db.get_all_batches()

        assert batches == []
        assert isinstance(batches, list)

    def test_get_all_batches_with_content(self, temp_workspace, sample_batch_content):
        """Test getting batches with actual content"""
        # Create a batch file
        batch_file = temp_workspace / "concepts" / "generated" / "20250101-001.md"
        batch_file.write_text(sample_batch_content)

        db = ConceptDatabase(temp_workspace)
        batches = db.get_all_batches()

        assert len(batches) == 1
        assert batches[0]['batch_id'] == '20250101-001'
        assert batches[0]['genre'] == 'Fantasy'
        assert batches[0]['count'] == 3
        assert batches[0]['location'] == 'generated'

    def test_get_all_batches_multiple_locations(self, temp_workspace, sample_batch_content):
        """Test getting batches from multiple subdirectories"""
        # Create batches in different locations
        (temp_workspace / "concepts" / "generated" / "batch1.md").write_text(
            sample_batch_content
        )
        (temp_workspace / "concepts" / "developing" / "batch2.md").write_text(
            sample_batch_content
        )
        (temp_workspace / "concepts" / "favorites" / "batch3.md").write_text(
            sample_batch_content
        )

        db = ConceptDatabase(temp_workspace)
        batches = db.get_all_batches()

        assert len(batches) == 3
        locations = [b['location'] for b in batches]
        assert 'generated' in locations
        assert 'developing' in locations
        assert 'favorites' in locations

    def test_get_batch_by_id(self, temp_workspace, sample_batch_content):
        """Test getting a specific batch by ID"""
        batch_file = temp_workspace / "concepts" / "generated" / "20250101-001.md"
        batch_file.write_text(sample_batch_content)

        db = ConceptDatabase(temp_workspace)
        batch = db.get_batch('20250101-001')

        assert batch is not None
        assert batch['batch_id'] == '20250101-001'

    def test_get_batch_nonexistent(self, temp_workspace):
        """Test getting a batch that doesn't exist"""
        db = ConceptDatabase(temp_workspace)
        # Use a valid batch ID format that doesn't exist
        batch = db.get_batch('20990101-999')

        assert batch is None

    def test_get_batch_invalid_format(self, temp_workspace):
        """Test getting a batch with invalid ID format raises error"""
        from aiwynns.validation import ValidationError

        db = ConceptDatabase(temp_workspace)

        with pytest.raises(ValidationError):
            db.get_batch('invalid-id')

    def test_get_all_stories_empty(self, temp_workspace):
        """Test getting stories from empty directory"""
        db = ConceptDatabase(temp_workspace)
        stories = db.get_all_stories()

        assert stories == []
        assert isinstance(stories, list)

    def test_get_all_stories_with_content(self, temp_workspace, sample_story_content):
        """Test getting stories with actual content"""
        story_file = temp_workspace / "stories" / "test-story.md"
        story_file.write_text(sample_story_content)

        db = ConceptDatabase(temp_workspace)
        stories = db.get_all_stories()

        assert len(stories) == 1
        assert stories[0]['story_id'] == 'test-story-001'
        assert stories[0]['title'] == 'Test Story'
        assert stories[0]['genre'] == 'Fantasy'

    def test_parse_batch_file_valid(self, temp_workspace, sample_batch_content):
        """Test parsing a valid batch file"""
        batch_file = temp_workspace / "concepts" / "generated" / "test.md"
        batch_file.write_text(sample_batch_content)

        db = ConceptDatabase(temp_workspace)
        batch = db._parse_batch_file(batch_file)

        assert batch is not None
        assert batch['batch_id'] == '20250101-001'
        assert batch['genre'] == 'Fantasy'
        assert 'concepts' in batch
        assert len(batch['concepts']) == 3

    def test_parse_batch_file_invalid_yaml(self, temp_workspace, invalid_yaml_content):
        """Test parsing a batch file with invalid YAML"""
        batch_file = temp_workspace / "concepts" / "generated" / "invalid.md"
        batch_file.write_text(invalid_yaml_content)

        db = ConceptDatabase(temp_workspace)
        batch = db._parse_batch_file(batch_file)

        # Should return None for invalid files
        assert batch is None

    def test_parse_story_file_valid(self, temp_workspace, sample_story_content):
        """Test parsing a valid story file"""
        story_file = temp_workspace / "stories" / "test.md"
        story_file.write_text(sample_story_content)

        db = ConceptDatabase(temp_workspace)
        story = db._parse_story_file(story_file)

        assert story is not None
        assert story['story_id'] == 'test-story-001'
        assert story['title'] == 'Test Story'

    def test_extract_concepts_from_content(self, temp_workspace):
        """Test extracting individual concepts from batch content"""
        content = """
## Concept 1: First Concept
Some content here

## Concept 2: Second Concept
More content here

## Concept 3: Third Concept
Even more content
"""
        db = ConceptDatabase(temp_workspace)
        concepts = db._extract_concepts_from_content(content)

        assert len(concepts) == 3
        assert concepts[0]['number'] == '1'
        assert concepts[0]['title'] == 'First Concept'
        assert concepts[1]['number'] == '2'
        assert concepts[1]['title'] == 'Second Concept'
        assert concepts[2]['number'] == '3'
        assert concepts[2]['title'] == 'Third Concept'

    def test_extract_concepts_no_concepts(self, temp_workspace):
        """Test extracting concepts from content with no concepts"""
        content = "Just some regular markdown content without concepts"

        db = ConceptDatabase(temp_workspace)
        concepts = db._extract_concepts_from_content(content)

        assert concepts == []

    def test_get_all_files(self, temp_workspace, sample_batch_content, sample_story_content):
        """Test getting all markdown files"""
        # Create some files
        (temp_workspace / "concepts" / "generated" / "batch1.md").write_text(
            sample_batch_content
        )
        (temp_workspace / "stories" / "story1.md").write_text(sample_story_content)

        db = ConceptDatabase(temp_workspace)
        files = db.get_all_files()

        assert len(files) == 2
        assert all(isinstance(f, Path) for f in files)
        assert all(f.suffix == '.md' for f in files)

    def test_concepts_dir_not_exists(self, tmp_path):
        """Test handling when concepts directory doesn't exist"""
        workspace = tmp_path / "empty_workspace"
        workspace.mkdir()

        db = ConceptDatabase(workspace)
        batches = db.get_all_batches()

        # Should return empty list, not crash
        assert batches == []

    def test_stories_dir_not_exists(self, tmp_path):
        """Test handling when stories directory doesn't exist"""
        workspace = tmp_path / "empty_workspace"
        workspace.mkdir()

        db = ConceptDatabase(workspace)
        stories = db.get_all_stories()

        # Should return empty list, not crash
        assert stories == []

    def test_batch_with_special_characters(self, temp_workspace):
        """Test batch with special characters in frontmatter"""
        content = """---
batch_id: 20250101-001
date_generated: 2025-01-01
genre: "Science Fiction & Fantasy"
tropes: "time travel, aliens, first contact"
count: 1
status: generated
llm_model: "Claude Sonnet 4.5"
---

## Concept 1: Test
Content
"""
        batch_file = temp_workspace / "concepts" / "generated" / "test.md"
        batch_file.write_text(content)

        db = ConceptDatabase(temp_workspace)
        batches = db.get_all_batches()

        assert len(batches) == 1
        assert batches[0]['genre'] == "Science Fiction & Fantasy"

    def test_batch_with_date_object(self, temp_workspace):
        """Test that date objects are preserved from YAML"""
        content = """---
batch_id: 20250101-001
date_generated: 2025-01-01
genre: Fantasy
tropes: magic
count: 1
status: generated
llm_model: Test
---

## Concept 1: Test
Content
"""
        batch_file = temp_workspace / "concepts" / "generated" / "test.md"
        batch_file.write_text(content)

        db = ConceptDatabase(temp_workspace)
        batch = db.get_batch('20250101-001')

        # date_generated should be a date object from YAML
        from datetime import date
        assert isinstance(batch['date_generated'], date)
