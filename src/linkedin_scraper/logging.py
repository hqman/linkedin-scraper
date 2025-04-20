import logging
import os
import sys
from datetime import datetime

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("linkedin_scraper")
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# file_handler = logging.FileHandler(f"logs/linkedin_scraper_{timestamp}.log")
# file_handler.setLevel(logging.DEBUG)

console_formatter = logging.Formatter("%(levelname)s: %(message)s")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

console_handler.setFormatter(console_formatter)
# file_handler.setFormatter(file_formatter)

logger.addHandler(console_handler)
# logger.addHandler(file_handler)

logger.propagate = False


def get_logger():
    return logger


LOGGER = get_logger()


def info(msg, *args, **kwargs):
    """Log an info message."""
    LOGGER.info(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    """Log an error message."""
    LOGGER.error(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    """Log a warning message."""
    LOGGER.warning(msg, *args, **kwargs)


def debug(msg, *args, **kwargs):
    """Log a debug message."""
    LOGGER.debug(msg, *args, **kwargs)


def critical(msg, *args, **kwargs):
    """Log a critical message."""
    LOGGER.critical(msg, *args, **kwargs)


def set_level(level):
    """Set the logging level."""
    LOGGER.setLevel(level)
