"""
Logging configuration module for the Movie Rating System.

This module sets up a structured logging configuration with:
- Proper format including timestamp, logger name, level, and message
- Console output handler
- INFO level as default
- Context-aware logging capabilities
"""

import logging
import sys
from typing import Optional


def setup_logging(
    name: str = "movie_rating",
    level: int = logging.INFO,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Set up and configure logging for the application.
    
    Args:
        name: Name of the logger (default: "movie_rating")
        level: Logging level (default: INFO)
        format_string: Custom format string for log messages
        
    Returns:
        Configured logger instance
    """
    # Default format if not provided
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers to avoid duplicates
    if logger.handlers:
        logger.handlers.clear()
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Create formatter and add it to the handler
    formatter = logging.Formatter(
        format_string,
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger


# Create the default logger instance
logger = setup_logging()


def get_logger(name: str = "movie_rating") -> logging.Logger:
    """
    Get or create a logger instance.
    
    Args:
        name: Name of the logger
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)
