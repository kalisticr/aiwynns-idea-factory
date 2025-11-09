"""
Tests for search.py - Search functionality
"""

import pytest
from aiwynns.search import SearchEngine
from aiwynns.validation import ValidationError


class TestSearchValidation:
    """Test validation in SearchEngine"""

    def test_search_empty_query(self, temp_workspace):
        """Test that empty query raises ValidationError"""
        from aiwynns.database import ConceptDatabase

        db = ConceptDatabase(temp_workspace)
        search = SearchEngine(db)

        with pytest.raises(ValidationError):
            search.search("")

    def test_search_none_query(self, temp_workspace):
        """Test that None query raises ValidationError"""
        from aiwynns.database import ConceptDatabase

        db = ConceptDatabase(temp_workspace)
        search = SearchEngine(db)

        with pytest.raises(ValidationError):
            search.search(None)

    def test_search_invalid_limit_negative(self, temp_workspace):
        """Test that negative limit raises ValidationError"""
        from aiwynns.database import ConceptDatabase

        db = ConceptDatabase(temp_workspace)
        search = SearchEngine(db)

        with pytest.raises(ValidationError):
            search.search("test", limit=-1)

    def test_search_invalid_limit_too_large(self, temp_workspace):
        """Test that limit > 1000 raises ValidationError"""
        from aiwynns.database import ConceptDatabase

        db = ConceptDatabase(temp_workspace)
        search = SearchEngine(db)

        with pytest.raises(ValidationError):
            search.search("test", limit=2000)

    def test_search_valid_inputs(self, temp_workspace):
        """Test that valid inputs work correctly"""
        from aiwynns.database import ConceptDatabase

        db = ConceptDatabase(temp_workspace)
        search = SearchEngine(db)

        # Should not raise
        results = search.search("test", genre="Fantasy", limit=10)
        assert isinstance(results, list)


class TestSearchFunctionality:
    """Test search functionality with sample data"""

    def test_search_returns_list(self, temp_workspace):
        """Test that search returns a list"""
        from aiwynns.database import ConceptDatabase

        db = ConceptDatabase(temp_workspace)
        search = SearchEngine(db)

        results = search.search("test")
        assert isinstance(results, list)

    def test_search_respects_limit(self, temp_workspace, sample_batch_content):
        """Test that search respects limit parameter"""
        from aiwynns.database import ConceptDatabase

        # Create multiple batch files
        for i in range(5):
            batch_file = temp_workspace / "concepts" / "generated" / f"batch{i}.md"
            batch_file.write_text(sample_batch_content)

        db = ConceptDatabase(temp_workspace)
        search = SearchEngine(db)

        # Search should return at most the limit
        results = search.search("Test", limit=2)
        assert len(results) <= 2

    def test_search_with_genre_filter(self, temp_workspace, sample_batch_content):
        """Test search with genre filter"""
        from aiwynns.database import ConceptDatabase

        batch_file = temp_workspace / "concepts" / "generated" / "batch1.md"
        batch_file.write_text(sample_batch_content)

        db = ConceptDatabase(temp_workspace)
        search = SearchEngine(db)

        # Search with matching genre
        results = search.search("Test", genre="Fantasy")
        assert isinstance(results, list)

        # Search with non-matching genre
        results = search.search("Test", genre="SciFi")
        assert isinstance(results, list)
