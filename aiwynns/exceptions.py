"""
Custom exception classes for Aiwynn's Idea Factory

Defines a hierarchy of domain-specific exceptions to provide
better error handling and more informative error messages.
"""


class IdeaFactoryError(Exception):
    """Base exception for all Idea Factory errors"""
    pass


# ============================================================================
# Validation Errors
# ============================================================================

class ValidationError(IdeaFactoryError):
    """Raised when input validation fails"""
    pass


# ============================================================================
# File System Errors
# ============================================================================

class FileSystemError(IdeaFactoryError):
    """Base exception for file system related errors"""
    pass


class TemplateNotFoundError(FileSystemError):
    """Raised when a required template file is not found"""
    def __init__(self, template_name: str, template_dir: str):
        self.template_name = template_name
        self.template_dir = template_dir
        super().__init__(
            f"Template file '{template_name}' not found in {template_dir}. "
            f"Please ensure templates are properly installed."
        )


class FileReadError(FileSystemError):
    """Raised when a file cannot be read"""
    def __init__(self, file_path: str, reason: str):
        self.file_path = file_path
        self.reason = reason
        super().__init__(
            f"Failed to read file '{file_path}': {reason}"
        )


class FileWriteError(FileSystemError):
    """Raised when a file cannot be written"""
    def __init__(self, file_path: str, reason: str):
        self.file_path = file_path
        self.reason = reason
        super().__init__(
            f"Failed to write file '{file_path}': {reason}"
        )


# ============================================================================
# Parsing Errors
# ============================================================================

class ParsingError(IdeaFactoryError):
    """Base exception for parsing errors"""
    pass


class InvalidFrontmatterError(ParsingError):
    """Raised when frontmatter cannot be parsed"""
    def __init__(self, file_path: str, reason: str):
        self.file_path = file_path
        self.reason = reason
        super().__init__(
            f"Invalid frontmatter in '{file_path}': {reason}"
        )


class MissingMetadataError(ParsingError):
    """Raised when required metadata is missing"""
    def __init__(self, file_path: str, missing_field: str):
        self.file_path = file_path
        self.missing_field = missing_field
        super().__init__(
            f"Missing required metadata field '{missing_field}' in '{file_path}'"
        )


# ============================================================================
# Resource Errors
# ============================================================================

class ResourceError(IdeaFactoryError):
    """Base exception for resource-related errors"""
    pass


class BatchNotFoundError(ResourceError):
    """Raised when a batch cannot be found"""
    def __init__(self, batch_id: str):
        self.batch_id = batch_id
        super().__init__(
            f"Batch '{batch_id}' not found. Use 'list-batches' to see available batches."
        )


class StoryNotFoundError(ResourceError):
    """Raised when a story cannot be found"""
    def __init__(self, story_name: str):
        self.story_name = story_name
        super().__init__(
            f"Story '{story_name}' not found. Use 'list-stories' to see available stories."
        )


class ConceptNotFoundError(ResourceError):
    """Raised when a concept cannot be found in a batch"""
    def __init__(self, batch_id: str, concept_number: int, total_concepts: int):
        self.batch_id = batch_id
        self.concept_number = concept_number
        self.total_concepts = total_concepts
        super().__init__(
            f"Concept #{concept_number} not found in batch '{batch_id}'. "
            f"This batch has {total_concepts} concepts (1-{total_concepts})."
        )


# ============================================================================
# Operation Errors
# ============================================================================

class OperationError(IdeaFactoryError):
    """Base exception for operation failures"""
    pass


class CreationError(OperationError):
    """Raised when creating a batch or story fails"""
    def __init__(self, resource_type: str, reason: str):
        self.resource_type = resource_type
        self.reason = reason
        super().__init__(
            f"Failed to create {resource_type}: {reason}"
        )


class SearchError(OperationError):
    """Raised when a search operation fails"""
    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(
            f"Search operation failed: {reason}"
        )


class ExportError(OperationError):
    """Raised when an export operation fails"""
    def __init__(self, format: str, reason: str):
        self.format = format
        self.reason = reason
        super().__init__(
            f"Failed to export to {format}: {reason}"
        )


# ============================================================================
# Configuration Errors
# ============================================================================

class ConfigurationError(IdeaFactoryError):
    """Base exception for configuration errors"""
    pass


class WorkspaceNotFoundError(ConfigurationError):
    """Raised when the workspace directory is not properly set up"""
    def __init__(self, workspace_path: str):
        self.workspace_path = workspace_path
        super().__init__(
            f"Workspace not properly configured at '{workspace_path}'. "
            f"Required directories (concepts/, stories/, templates/) may be missing."
        )


class InvalidWorkspaceError(ConfigurationError):
    """Raised when the workspace structure is invalid"""
    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(
            f"Invalid workspace structure: {reason}"
        )
