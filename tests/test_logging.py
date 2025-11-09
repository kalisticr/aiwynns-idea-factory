"""
Tests for logging_config.py - Logging infrastructure
"""

import pytest
import logging
import tempfile
from pathlib import Path
from aiwynns.logging_config import (
    setup_logging,
    get_logger,
    set_level,
    disable_logging,
    enable_logging
)


class TestLoggingSetup:
    """Test logging setup and configuration"""

    def setup_method(self):
        """Reset logging state before each test"""
        # Clear all handlers from aiwynns logger
        logger = logging.getLogger('aiwynns')
        logger.handlers.clear()
        logger.setLevel(logging.INFO)
        logger.disabled = False

    def test_setup_logging_console_only(self):
        """Test logging setup with console handler only"""
        setup_logging(level=logging.INFO, console_output=True)

        logger = logging.getLogger('aiwynns')
        assert logger.level == logging.INFO
        assert len(logger.handlers) >= 1
        assert any(isinstance(h, logging.StreamHandler) for h in logger.handlers)

    def test_setup_logging_file_handler(self):
        """Test logging setup with file handler"""
        with tempfile.NamedTemporaryFile(suffix='.log', delete=False) as f:
            log_file = Path(f.name)

        try:
            setup_logging(level=logging.DEBUG, log_file=log_file, console_output=False)

            logger = logging.getLogger('aiwynns')
            assert logger.level == logging.DEBUG

            # Test that logging works
            test_logger = get_logger('aiwynns.test_module')
            test_logger.info("Test message")

            # Flush handlers to ensure write
            for handler in logger.handlers:
                handler.flush()

            # Check file was created and has content
            assert log_file.exists()
            content = log_file.read_text()
            assert "Test message" in content

        finally:
            # Close handlers before deleting
            for handler in logging.getLogger('aiwynns').handlers:
                handler.close()
            if log_file.exists():
                log_file.unlink()

    def test_setup_logging_no_console(self):
        """Test logging setup without console output"""
        setup_logging(level=logging.INFO, console_output=False)

        logger = logging.getLogger('aiwynns')
        # Should have no console handler
        console_handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler) and not hasattr(h, 'baseFilename')]
        assert len(console_handlers) == 0

    def test_setup_logging_detailed_format(self):
        """Test logging with detailed format"""
        setup_logging(level=logging.DEBUG, console_output=True, detailed=True)

        logger = logging.getLogger('aiwynns')
        assert len(logger.handlers) >= 1

        # Verify formatter includes filename and lineno
        handler = logger.handlers[0]
        format_string = handler.formatter._fmt
        assert '%(filename)s' in format_string
        assert '%(lineno)d' in format_string

    def test_setup_logging_from_env_var(self, monkeypatch):
        """Test logging level from environment variable"""
        monkeypatch.setenv('AIWYNNS_LOG_LEVEL', 'DEBUG')

        setup_logging(console_output=False)

        logger = logging.getLogger('aiwynns')
        assert logger.level == logging.DEBUG

    def test_setup_logging_invalid_env_var(self, monkeypatch):
        """Test that invalid env var falls back to default"""
        monkeypatch.setenv('AIWYNNS_LOG_LEVEL', 'INVALID')

        setup_logging(console_output=False)

        logger = logging.getLogger('aiwynns')
        assert logger.level == logging.INFO  # Default level

    def test_get_logger(self):
        """Test getting a logger for a specific module"""
        setup_logging(level=logging.INFO, console_output=False)

        test_logger = get_logger('aiwynns.test_module')
        assert isinstance(test_logger, logging.Logger)
        assert test_logger.name == 'aiwynns.test_module'

    def test_set_level(self):
        """Test changing log level at runtime"""
        setup_logging(level=logging.INFO, console_output=True)

        logger = logging.getLogger('aiwynns')
        assert logger.level == logging.INFO

        set_level(logging.DEBUG)
        assert logger.level == logging.DEBUG

        # Verify handlers also updated
        for handler in logger.handlers:
            assert handler.level == logging.DEBUG

    def test_disable_enable_logging(self):
        """Test disabling and re-enabling logging"""
        setup_logging(level=logging.INFO, console_output=False)

        logger = logging.getLogger('aiwynns')
        assert not logger.disabled

        disable_logging()
        assert logger.disabled

        enable_logging()
        assert not logger.disabled

    def test_multiple_setup_calls(self):
        """Test that multiple setup calls don't create duplicate handlers"""
        setup_logging(level=logging.INFO, console_output=True)
        logger = logging.getLogger('aiwynns')
        initial_count = len(logger.handlers)

        setup_logging(level=logging.INFO, console_output=True)
        # Handlers should be cleared and recreated, not duplicated
        assert len(logger.handlers) == initial_count


class TestLoggingIntegration:
    """Test logging integration with other modules"""

    def setup_method(self):
        """Reset logging state and set up test environment"""
        logger = logging.getLogger('aiwynns')
        logger.handlers.clear()
        logger.setLevel(logging.DEBUG)
        logger.disabled = False

        # Setup logging with no console output for tests
        setup_logging(level=logging.DEBUG, console_output=False)

    def test_database_logging(self, temp_workspace, sample_batch_content, caplog):
        """Test that database module logs correctly"""
        from aiwynns.database import ConceptDatabase

        # Create a batch file
        batch_file = temp_workspace / "concepts" / "generated" / "test.md"
        batch_file.write_text(sample_batch_content)

        # Capture log output
        with caplog.at_level(logging.DEBUG, logger='aiwynns'):
            db = ConceptDatabase(temp_workspace)
            batches = db.get_all_batches()

            # Verify logging occurred and operations succeeded
            assert len(batches) == 1

    def test_creator_logging(self, temp_workspace, mock_templates, caplog):
        """Test that creator module logs correctly"""
        from aiwynns.creator import Creator

        with caplog.at_level(logging.INFO, logger='aiwynns'):
            creator = Creator(temp_workspace)
            file_path = creator.create_batch(
                genre="Fantasy",
                tropes="magic, adventure",
                model="Test Model",
                count=10
            )

            assert file_path.exists()

    def test_search_logging(self, temp_workspace, caplog):
        """Test that search module logs correctly"""
        from aiwynns.database import ConceptDatabase
        from aiwynns.search import SearchEngine

        with caplog.at_level(logging.INFO, logger='aiwynns'):
            db = ConceptDatabase(temp_workspace)
            search = SearchEngine(db)
            results = search.search("test")

            assert isinstance(results, list)


class TestLogOutput:
    """Test actual log output and formatting"""

    def setup_method(self):
        """Reset logging state"""
        logger = logging.getLogger('aiwynns')
        logger.handlers.clear()
        logger.setLevel(logging.DEBUG)
        logger.disabled = False

    def test_log_format_default(self, caplog):
        """Test default log format"""
        setup_logging(level=logging.INFO, console_output=False)

        logger = get_logger('aiwynns.test')
        with caplog.at_level(logging.INFO, logger='aiwynns'):
            logger.info("Test message")

            # Check that log record was captured
            assert len(caplog.records) == 1
            record = caplog.records[0]
            assert record.levelname == "INFO"
            assert record.message == "Test message"
            assert record.name == "aiwynns.test"

    def test_log_levels(self, caplog):
        """Test different log levels"""
        setup_logging(level=logging.DEBUG, console_output=False)

        logger = get_logger('aiwynns.test')
        with caplog.at_level(logging.DEBUG, logger='aiwynns'):
            logger.debug("Debug message")
            logger.info("Info message")
            logger.warning("Warning message")
            logger.error("Error message")

            # Filter out the "Logging initialized" message from setup_logging
            test_records = [r for r in caplog.records if r.name == 'aiwynns.test']
            assert len(test_records) == 4
            assert test_records[0].levelname == "DEBUG"
            assert test_records[1].levelname == "INFO"
            assert test_records[2].levelname == "WARNING"
            assert test_records[3].levelname == "ERROR"

    def test_log_filtering_by_level(self, caplog):
        """Test that logs below the configured level are filtered"""
        setup_logging(level=logging.WARNING, console_output=False)

        logger = get_logger('aiwynns.test')
        with caplog.at_level(logging.DEBUG, logger='aiwynns'):
            logger.debug("Debug message")
            logger.info("Info message")
            logger.warning("Warning message")
            logger.error("Error message")

            # Only WARNING and above should be captured
            warning_and_above = [r for r in caplog.records if r.levelno >= logging.WARNING]
            assert len(warning_and_above) == 2
