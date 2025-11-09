"""
Input validation utilities for the Idea Factory
"""

import re
from typing import Optional


class ValidationError(Exception):
    """Raised when input validation fails"""
    pass


def validate_string(
    value: str,
    field_name: str,
    min_length: int = 1,
    max_length: int = 500,
    allow_empty: bool = False
) -> str:
    """
    Validate a string input

    Args:
        value: The string to validate
        field_name: Name of the field for error messages
        min_length: Minimum allowed length
        max_length: Maximum allowed length
        allow_empty: Whether to allow empty strings

    Returns:
        The validated string (stripped of whitespace)

    Raises:
        ValidationError: If validation fails
    """
    if value is None:
        raise ValidationError(f"{field_name} cannot be None")

    if not isinstance(value, str):
        raise ValidationError(f"{field_name} must be a string, got {type(value).__name__}")

    # Strip whitespace
    value = value.strip()

    if len(value) == 0:
        if not allow_empty:
            raise ValidationError(f"{field_name} cannot be empty")
        else:
            return value  # Return early if empty and allowed

    if len(value) < min_length:
        raise ValidationError(
            f"{field_name} must be at least {min_length} characters, got {len(value)}"
        )

    if len(value) > max_length:
        raise ValidationError(
            f"{field_name} must be at most {max_length} characters, got {len(value)}"
        )

    return value


def validate_integer(
    value: int,
    field_name: str,
    min_value: Optional[int] = None,
    max_value: Optional[int] = None
) -> int:
    """
    Validate an integer input

    Args:
        value: The integer to validate
        field_name: Name of the field for error messages
        min_value: Minimum allowed value (inclusive)
        max_value: Maximum allowed value (inclusive)

    Returns:
        The validated integer

    Raises:
        ValidationError: If validation fails
    """
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValidationError(f"{field_name} must be an integer, got {type(value).__name__}")

    if min_value is not None and value < min_value:
        raise ValidationError(f"{field_name} must be at least {min_value}, got {value}")

    if max_value is not None and value > max_value:
        raise ValidationError(f"{field_name} must be at most {max_value}, got {value}")

    return value


def validate_batch_id(batch_id: str) -> str:
    """
    Validate a batch ID format (YYYYMMDD-NNN)

    Args:
        batch_id: The batch ID to validate

    Returns:
        The validated batch ID

    Raises:
        ValidationError: If format is invalid
    """
    batch_id = validate_string(batch_id, "batch_id", min_length=12, max_length=12)

    pattern = r'^\d{8}-\d{3}$'
    if not re.match(pattern, batch_id):
        raise ValidationError(
            f"batch_id must match format YYYYMMDD-NNN, got '{batch_id}'"
        )

    return batch_id


def validate_slug(slug: str, field_name: str = "slug") -> str:
    """
    Validate a URL-safe slug

    Args:
        slug: The slug to validate
        field_name: Name of the field for error messages

    Returns:
        The validated slug

    Raises:
        ValidationError: If slug is invalid
    """
    slug = validate_string(slug, field_name, min_length=1, max_length=200)

    # Slug must contain only lowercase letters, numbers, and hyphens
    if not re.match(r'^[a-z0-9-]+$', slug):
        raise ValidationError(
            f"{field_name} must contain only lowercase letters, numbers, and hyphens"
        )

    # Must not start or end with hyphen
    if slug.startswith('-') or slug.endswith('-'):
        raise ValidationError(f"{field_name} cannot start or end with a hyphen")

    return slug


def sanitize_search_query(query: str) -> str:
    """
    Sanitize a search query string

    Args:
        query: The search query to sanitize

    Returns:
        Sanitized query string

    Raises:
        ValidationError: If query is invalid
    """
    if query is None or (isinstance(query, str) and len(query.strip()) == 0):
        raise ValidationError("Search query cannot be empty")

    query = validate_string(query, "search query", min_length=1, max_length=1000)

    # Remove potentially problematic characters for regex/fuzzy matching
    # Keep alphanumeric, spaces, and basic punctuation
    query = re.sub(r'[^\w\s\-.,!?\'\"]+', '', query)

    return query


def validate_limit(limit: int) -> int:
    """
    Validate a limit parameter for result sets

    Args:
        limit: The limit value to validate

    Returns:
        The validated limit

    Raises:
        ValidationError: If limit is invalid
    """
    return validate_integer(limit, "limit", min_value=1, max_value=1000)
