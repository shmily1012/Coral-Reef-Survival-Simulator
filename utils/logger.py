"""
Logging Module

Provides centralized logging functionality for the entire application.
Handles different log levels, file output, and formatted messages.

Features:
- Multiple log levels (DEBUG, INFO, WARNING, ERROR)
- File and console output
- Timestamp and context information
- Color-coded console output
- Rotation of log files
- Line numbers and function names in logs
"""

import logging
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
import traceback

# ANSI color codes for console output
COLORS = {
    'DEBUG': '\033[94m',    # Blue
    'INFO': '\033[92m',     # Green
    'WARNING': '\033[93m',  # Yellow
    'ERROR': '\033[91m',    # Red
    'ENDC': '\033[0m'       # Reset color
}

class ColoredFormatter(logging.Formatter):
    """Custom formatter adding colors to log levels for console output."""
    
    def format(self, record):
        if record.levelname in COLORS:
            record.levelname = f"{COLORS[record.levelname]}{record.levelname}{COLORS['ENDC']}"
        return super().format(record)

def setup_logger(name='coral_reef_simulator'):
    """
    Set up and configure the logger.
    
    Args:
        name (str): Name of the logger instance
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Create formatters with line numbers and function names
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d:%(funcName)s - %(message)s'
    )
    
    console_formatter = ColoredFormatter(
        '%(levelname)s - %(filename)s:%(lineno)d:%(funcName)s - %(message)s'
    )
    
    # File handler (with rotation)
    log_file = f'logs/{name}_{datetime.now().strftime("%Y%m%d")}.log'
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5*1024*1024,  # 5MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(file_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(console_formatter)
    
    # Remove any existing handlers
    logger.handlers = []
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Create a default logger instance
logger = setup_logger()

def log_exception(e, context=""):
    """
    Log an exception with full traceback.
    
    Args:
        e (Exception): The exception to log
        context (str): Additional context information
    """
    error_msg = f"{context} - {str(e)}\n{traceback.format_exc()}"
    logger.error(error_msg) 