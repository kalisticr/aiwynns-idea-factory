"""
Tests for exceptions.py - Custom exception classes
"""

import pytest
from pathlib import Path
from aiwynns.exceptions import (
    IdeaFactoryError,
    ValidationError,
    FileSystemError,
    TemplateNotFoundError,
    FileReadError,
    FileWriteError,
    ParsingError,
    InvalidFrontmatterError,
    MissingMetadataError,
    ResourceError,
    BatchNotFoundError,
    StoryNotFoundError,
    ConceptNotFoundError,
    OperationError,
    CreationError,
    SearchError,
    ExportError,
    ConfigurationError,
    WorkspaceNotFoundError,
    InvalidWorkspaceError
)


class TestExceptionHierarchy:
    """Test exception inheritance hierarchy"""

    def test_all_inherit_from_base(self):
        """Test that all custom exceptions inherit from IdeaFactoryError"""
        exceptions = [
            ValidationError,
            FileSystemError,
            TemplateNotFoundError,
            FileReadError,
            FileWriteError,
            ParsingError,
            InvalidFrontmatterError,
            MissingMetadataError,
            ResourceError,
            BatchNotFoundError,
            StoryNotFoundError,
            ConceptNotFoundError,
            OperationError,
            CreationError,
            SearchError,
            ExportError,
            ConfigurationError,
            WorkspaceNotFoundError,
            InvalidWorkspaceError
        ]

        for exc_class in exceptions:
            assert issubclass(exc_class, IdeaFactoryError)

    def test_base_inherits_from_exception(self):
        """Test that base exception inherits from Exception"""
        assert issubclass(IdeaFactoryError, Exception)

    def test_filesystem_hierarchy(self):
        """Test FileSystem exception hierarchy"""
        assert issubclass(TemplateNotFoundError, FileSystemError)
        assert issubclass(FileReadError, FileSystemError)
        assert issubclass(FileWriteError, FileSystemError)

    def test_parsing_hierarchy(self):
        """Test Parsing exception hierarchy"""
        assert issubclass(InvalidFrontmatterError, ParsingError)
        assert issubclass(MissingMetadataError, ParsingError)

    def test_resource_hierarchy(self):
        """Test Resource exception hierarchy"""
        assert issubclass(BatchNotFoundError, ResourceError)
        assert issubclass(StoryNotFoundError, ResourceError)
        assert issubclass(ConceptNotFoundError, ResourceError)

    def test_operation_hierarchy(self):
        """Test Operation exception hierarchy"""
        assert issubclass(CreationError, OperationError)
        assert issubclass(SearchError, OperationError)
        assert issubclass(ExportError, OperationError)

    def test_configuration_hierarchy(self):
        """Test Configuration exception hierarchy"""
        assert issubclass(WorkspaceNotFoundError, ConfigurationError)
        assert issubclass(InvalidWorkspaceError, ConfigurationError)


class TestValidationError:
    """Test ValidationError"""

    def test_validation_error_message(self):
        """Test ValidationError with custom message"""
        err = ValidationError("Invalid input")
        assert str(err) == "Invalid input"

    def test_validation_error_catchable(self):
        """Test ValidationError can be caught"""
        with pytest.raises(ValidationError) as exc_info:
            raise ValidationError("Test error")

        assert "Test error" in str(exc_info.value)


class TestFileSystemErrors:
    """Test FileSystem exceptions"""

    def test_template_not_found_error(self):
        """Test TemplateNotFoundError provides useful message"""
        err = TemplateNotFoundError("test-template.md", "/path/to/templates")

        assert "test-template.md" in str(err)
        assert "/path/to/templates" in str(err)
        assert "not found" in str(err).lower()
        assert err.template_name == "test-template.md"
        assert err.template_dir == "/path/to/templates"

    def test_file_read_error(self):
        """Test FileReadError provides useful message"""
        err = FileReadError("/path/to/file.md", "Permission denied")

        assert "/path/to/file.md" in str(err)
        assert "Permission denied" in str(err)
        assert "read" in str(err).lower()
        assert err.file_path == "/path/to/file.md"
        assert err.reason == "Permission denied"

    def test_file_write_error(self):
        """Test FileWriteError provides useful message"""
        err = FileWriteError("/path/to/file.md", "Disk full")

        assert "/path/to/file.md" in str(err)
        assert "Disk full" in str(err)
        assert "write" in str(err).lower()
        assert err.file_path == "/path/to/file.md"
        assert err.reason == "Disk full"


class TestParsingErrors:
    """Test Parsing exceptions"""

    def test_invalid_frontmatter_error(self):
        """Test InvalidFrontmatterError provides useful message"""
        err = InvalidFrontmatterError("/path/to/file.md", "Invalid YAML syntax")

        assert "/path/to/file.md" in str(err)
        assert "Invalid YAML syntax" in str(err)
        assert "frontmatter" in str(err).lower()
        assert err.file_path == "/path/to/file.md"
        assert err.reason == "Invalid YAML syntax"

    def test_missing_metadata_error(self):
        """Test MissingMetadataError provides useful message"""
        err = MissingMetadataError("/path/to/file.md", "batch_id")

        assert "/path/to/file.md" in str(err)
        assert "batch_id" in str(err)
        assert "missing" in str(err).lower()
        assert err.file_path == "/path/to/file.md"
        assert err.missing_field == "batch_id"


class TestResourceErrors:
    """Test Resource exceptions"""

    def test_batch_not_found_error(self):
        """Test BatchNotFoundError provides useful message"""
        err = BatchNotFoundError("20250101-001")

        assert "20250101-001" in str(err)
        assert "not found" in str(err).lower()
        assert "list-batches" in str(err).lower()
        assert err.batch_id == "20250101-001"

    def test_story_not_found_error(self):
        """Test StoryNotFoundError provides useful message"""
        err = StoryNotFoundError("my-story")

        assert "my-story" in str(err)
        assert "not found" in str(err).lower()
        assert "list-stories" in str(err).lower()
        assert err.story_name == "my-story"

    def test_concept_not_found_error(self):
        """Test ConceptNotFoundError provides useful message"""
        err = ConceptNotFoundError("20250101-001", 11, 10)

        assert "20250101-001" in str(err)
        assert "11" in str(err)
        assert "10" in str(err)
        assert "not found" in str(err).lower()
        assert err.batch_id == "20250101-001"
        assert err.concept_number == 11
        assert err.total_concepts == 10


class TestOperationErrors:
    """Test Operation exceptions"""

    def test_creation_error(self):
        """Test CreationError provides useful message"""
        err = CreationError("batch", "Template not found")

        assert "batch" in str(err)
        assert "Template not found" in str(err)
        assert "create" in str(err).lower()
        assert err.resource_type == "batch"
        assert err.reason == "Template not found"

    def test_search_error(self):
        """Test SearchError provides useful message"""
        err = SearchError("Invalid query syntax")

        assert "Invalid query syntax" in str(err)
        assert "search" in str(err).lower()
        assert err.reason == "Invalid query syntax"

    def test_export_error(self):
        """Test ExportError provides useful message"""
        err = ExportError("JSON", "Invalid data structure")

        assert "JSON" in str(err)
        assert "Invalid data structure" in str(err)
        assert "export" in str(err).lower()
        assert err.format == "JSON"
        assert err.reason == "Invalid data structure"


class TestConfigurationErrors:
    """Test Configuration exceptions"""

    def test_workspace_not_found_error(self):
        """Test WorkspaceNotFoundError provides useful message"""
        err = WorkspaceNotFoundError("/path/to/workspace")

        assert "/path/to/workspace" in str(err)
        assert "workspace" in str(err).lower()
        assert "not properly configured" in str(err).lower()
        assert err.workspace_path == "/path/to/workspace"

    def test_invalid_workspace_error(self):
        """Test InvalidWorkspaceError provides useful message"""
        err = InvalidWorkspaceError("Missing templates directory")

        assert "Missing templates directory" in str(err)
        assert "invalid" in str(err).lower()
        assert "workspace" in str(err).lower()
        assert err.reason == "Missing templates directory"


class TestExceptionCatching:
    """Test exception catching patterns"""

    def test_catch_specific_exception(self):
        """Test catching specific exception type"""
        with pytest.raises(BatchNotFoundError):
            raise BatchNotFoundError("test-batch")

    def test_catch_by_category(self):
        """Test catching by exception category"""
        # All FileSystem errors can be caught as FileSystemError
        with pytest.raises(FileSystemError):
            raise TemplateNotFoundError("test.md", "/templates")

        with pytest.raises(FileSystemError):
            raise FileReadError("test.md", "error")

    def test_catch_all_idea_factory_errors(self):
        """Test catching all custom exceptions"""
        # Any custom exception can be caught as IdeaFactoryError
        with pytest.raises(IdeaFactoryError):
            raise ValidationError("test error")

        with pytest.raises(IdeaFactoryError):
            raise BatchNotFoundError("test-batch")

        with pytest.raises(IdeaFactoryError):
            raise FileReadError("file.md", "error")


class TestExceptionUsability:
    """Test that exceptions are easy to use in practice"""

    def test_can_add_context_to_exceptions(self):
        """Test that exceptions can carry additional context"""
        err = TemplateNotFoundError("test.md", "/templates")

        # Check that we can access attributes
        assert hasattr(err, 'template_name')
        assert hasattr(err, 'template_dir')
        assert err.template_name == "test.md"

    def test_exceptions_are_informative(self):
        """Test that error messages guide users to solutions"""
        err = BatchNotFoundError("20250101-001")

        message = str(err)
        # Should mention what to do
        assert "list-batches" in message.lower()
        # Should be clear about what went wrong
        assert "not found" in message.lower()
        # Should include the problematic value
        assert "20250101-001" in message
