"""
Logging configuration for Aiwynn's Idea Factory

Provides centralized logging setup with configurable levels and handlers.
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional


# Default log format
DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DETAILED_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"

# Default log level
DEFAULT_LEVEL = logging.INFO


def setup_logging(
    level: Optional[int] = None,
    log_file: Optional[Path] = None,
    console_output: bool = True,
    detailed: bool = False
) -> None:
    """
    Configure logging for the application

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to log file
        console_output: Whether to output logs to console
        detailed: Whether to use detailed log format with file/line info

    Environment Variables:
        AIWYNNS_LOG_LEVEL: Override default log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        AIWYNNS_LOG_FILE: Override default log file path
    """
    import os

    # Determine log level from environment or parameter
    if level is None:
        env_level = os.getenv('AIWYNNS_LOG_LEVEL', '').upper()
        level = getattr(logging, env_level, DEFAULT_LEVEL) if env_level else DEFAULT_LEVEL

    # Determine log file from environment or parameter
    if log_file is None:
        env_log_file = os.getenv('AIWYNNS_LOG_FILE')
        if env_log_file:
            log_file = Path(env_log_file)

    # Get root logger for aiwynns package
    logger = logging.getLogger('aiwynns')
    logger.setLevel(level)

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()

    # Choose format
    log_format = DETAILED_FORMAT if detailed else DEFAULT_FORMAT
    formatter = logging.Formatter(log_format)

    # Console handler (stderr to not interfere with stdout output)
    if console_output:
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # File handler with rotation
    if log_file:
        try:
            # Create log directory if it doesn't exist
            log_file.parent.mkdir(parents=True, exist_ok=True)

            # Rotating file handler (10MB max, keep 5 backups)
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=5,
                encoding='utf-8'
            )
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        except (OSError, PermissionError) as e:
            # If we can't write to log file, just warn and continue
            if console_output:
                logger.warning(f"Could not create log file {log_file}: {e}")

    logger.debug(f"Logging initialized at level {logging.getLevelName(level)}")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger for a specific module

    Args:
        name: Module name (typically __name__)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


def set_level(level: int) -> None:
    """
    Change the log level at runtime

    Args:
        level: New logging level (e.g., logging.DEBUG)
    """
    logger = logging.getLogger('aiwynns')
    logger.setLevel(level)
    for handler in logger.handlers:
        handler.setLevel(level)


def disable_logging() -> None:
    """Disable all logging (useful for tests)"""
    logging.getLogger('aiwynns').disabled = True


def enable_logging() -> None:
    """Re-enable logging after it was disabled"""
    logging.getLogger('aiwynns').disabled = False
