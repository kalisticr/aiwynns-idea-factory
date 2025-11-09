"""
Tests for validation.py - Input validation utilities
"""

import pytest
from aiwynns.validation import (
    validate_string,
    validate_integer,
    validate_batch_id,
    validate_slug,
    sanitize_search_query,
    validate_limit,
    ValidationError
)


class TestValidateString:
    """Test string validation"""

    def test_valid_string(self):
        """Test validating a normal string"""
        result = validate_string("Test String", "test_field")
        assert result == "Test String"

    def test_strips_whitespace(self):
        """Test that whitespace is stripped"""
        result = validate_string("  Test String  ", "test_field")
        assert result == "Test String"

    def test_none_value(self):
        """Test that None raises error"""
        with pytest.raises(ValidationError) as exc_info:
            validate_string(None, "test_field")
        assert "cannot be None" in str(exc_info.value)

    def test_non_string_type(self):
        """Test that non-string types raise error"""
        with pytest.raises(ValidationError) as exc_info:
            validate_string(123, "test_field")
        assert "must be a string" in str(exc_info.value)

    def test_empty_string_not_allowed(self):
        """Test that empty strings raise error by default"""
        with pytest.raises(ValidationError) as exc_info:
            validate_string("", "test_field")
        assert "cannot be empty" in str(exc_info.value)

    def test_empty_string_allowed(self):
        """Test that empty strings can be allowed"""
        result = validate_string("", "test_field", allow_empty=True)
        assert result == ""

    def test_min_length(self):
        """Test minimum length validation"""
        with pytest.raises(ValidationError) as exc_info:
            validate_string("ab", "test_field", min_length=3)
        assert "at least 3 characters" in str(exc_info.value)

    def test_max_length(self):
        """Test maximum length validation"""
        with pytest.raises(ValidationError) as exc_info:
            validate_string("abcdef", "test_field", max_length=5)
        assert "at most 5 characters" in str(exc_info.value)


class TestValidateInteger:
    """Test integer validation"""

    def test_valid_integer(self):
        """Test validating a normal integer"""
        result = validate_integer(42, "test_field")
        assert result == 42

    def test_non_integer_type(self):
        """Test that non-integer types raise error"""
        with pytest.raises(ValidationError) as exc_info:
            validate_integer("123", "test_field")
        assert "must be an integer" in str(exc_info.value)

    def test_boolean_rejected(self):
        """Test that booleans are rejected (even though they're technically ints)"""
        with pytest.raises(ValidationError):
            validate_integer(True, "test_field")

    def test_min_value(self):
        """Test minimum value validation"""
        with pytest.raises(ValidationError) as exc_info:
            validate_integer(5, "test_field", min_value=10)
        assert "at least 10" in str(exc_info.value)

    def test_max_value(self):
        """Test maximum value validation"""
        with pytest.raises(ValidationError) as exc_info:
            validate_integer(15, "test_field", max_value=10)
        assert "at most 10" in str(exc_info.value)

    def test_negative_values(self):
        """Test that negative values work with proper bounds"""
        result = validate_integer(-5, "test_field", min_value=-10, max_value=0)
        assert result == -5


class TestValidateBatchId:
    """Test batch ID validation"""

    def test_valid_batch_id(self):
        """Test validating a correct batch ID"""
        result = validate_batch_id("20250101-001")
        assert result == "20250101-001"

    def test_invalid_format_no_dash(self):
        """Test that IDs without dash are rejected"""
        with pytest.raises(ValidationError):
            validate_batch_id("20250101001")

    def test_invalid_format_wrong_length(self):
        """Test that IDs with wrong length are rejected"""
        with pytest.raises(ValidationError) as exc_info:
            validate_batch_id("2025-001")
        assert "12" in str(exc_info.value)

    def test_invalid_format_letters(self):
        """Test that IDs with letters are rejected"""
        with pytest.raises(ValidationError) as exc_info:
            validate_batch_id("2025ABCD-001")
        assert "must match format YYYYMMDD-NNN" in str(exc_info.value)

    def test_invalid_format_wrong_number_length(self):
        """Test that IDs with wrong number part are rejected"""
        with pytest.raises(ValidationError):
            validate_batch_id("20250101-01")


class TestValidateSlug:
    """Test slug validation"""

    def test_valid_slug(self):
        """Test validating a correct slug"""
        result = validate_slug("my-test-slug-123")
        assert result == "my-test-slug-123"

    def test_uppercase_rejected(self):
        """Test that uppercase letters are rejected"""
        with pytest.raises(ValidationError) as exc_info:
            validate_slug("My-Test-Slug")
        assert "lowercase letters, numbers, and hyphens" in str(exc_info.value)

    def test_special_characters_rejected(self):
        """Test that special characters are rejected"""
        with pytest.raises(ValidationError):
            validate_slug("test_slug!")

    def test_starts_with_hyphen(self):
        """Test that slugs starting with hyphen are rejected"""
        with pytest.raises(ValidationError) as exc_info:
            validate_slug("-test-slug")
        assert "cannot start or end with a hyphen" in str(exc_info.value)

    def test_ends_with_hyphen(self):
        """Test that slugs ending with hyphen are rejected"""
        with pytest.raises(ValidationError) as exc_info:
            validate_slug("test-slug-")
        assert "cannot start or end with a hyphen" in str(exc_info.value)

    def test_empty_slug(self):
        """Test that empty slugs are rejected"""
        with pytest.raises(ValidationError):
            validate_slug("")


class TestSanitizeSearchQuery:
    """Test search query sanitization"""

    def test_valid_query(self):
        """Test sanitizing a normal query"""
        result = sanitize_search_query("magic sword quest")
        assert result == "magic sword quest"

    def test_strips_whitespace(self):
        """Test that whitespace is stripped"""
        result = sanitize_search_query("  test query  ")
        assert result == "test query"

    def test_empty_query(self):
        """Test that empty queries raise error"""
        with pytest.raises(ValidationError) as exc_info:
            sanitize_search_query("")
        assert "cannot be empty" in str(exc_info.value)

    def test_none_query(self):
        """Test that None queries raise error"""
        with pytest.raises(ValidationError) as exc_info:
            sanitize_search_query(None)
        assert "cannot be empty" in str(exc_info.value)

    def test_removes_dangerous_characters(self):
        """Test that potentially dangerous characters are removed"""
        result = sanitize_search_query("test@#$%query")
        assert "@" not in result
        assert "#" not in result
        assert "$" not in result
        assert "%"  not in result

    def test_keeps_basic_punctuation(self):
        """Test that basic punctuation is kept"""
        result = sanitize_search_query("test, query! what's this?")
        assert "," in result
        assert "!" in result
        assert "?" in result
        assert "'" in result

    def test_max_length(self):
        """Test that extremely long queries are rejected"""
        long_query = "a" * 1001
        with pytest.raises(ValidationError) as exc_info:
            sanitize_search_query(long_query)
        assert "at most 1000 characters" in str(exc_info.value)


class TestValidateLimit:
    """Test limit validation"""

    def test_valid_limit(self):
        """Test validating a normal limit"""
        result = validate_limit(20)
        assert result == 20

    def test_minimum_limit(self):
        """Test that limit must be at least 1"""
        with pytest.raises(ValidationError) as exc_info:
            validate_limit(0)
        assert "at least 1" in str(exc_info.value)

    def test_negative_limit(self):
        """Test that negative limits are rejected"""
        with pytest.raises(ValidationError):
            validate_limit(-5)

    def test_maximum_limit(self):
        """Test that limit cannot exceed 1000"""
        with pytest.raises(ValidationError) as exc_info:
            validate_limit(1001)
        assert "at most 1000" in str(exc_info.value)


class TestValidationIntegration:
    """Test validation in real-world scenarios"""

    def test_batch_creation_inputs(self):
        """Test typical batch creation inputs"""
        genre = validate_string("Fantasy", "genre", max_length=100)
        tropes = validate_string("magic, adventure", "tropes", max_length=500)
        model = validate_string("Claude Sonnet 4.5", "model", max_length=100)
        count = validate_integer(10, "count", min_value=1, max_value=50)

        assert genre == "Fantasy"
        assert tropes == "magic, adventure"
        assert model == "Claude Sonnet 4.5"
        assert count == 10

    def test_search_inputs(self):
        """Test typical search inputs"""
        query = sanitize_search_query("magic sword")
        limit = validate_limit(20)

        assert query == "magic sword"
        assert limit == 20

    def test_batch_id_lookup(self):
        """Test typical batch ID lookup"""
        batch_id = validate_batch_id("20250108-001")
        assert batch_id == "20250108-001"
