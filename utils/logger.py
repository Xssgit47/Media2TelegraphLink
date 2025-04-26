"""
Logger configuration
"""
import os
import sys
import logging
from pathlib import Path

def setup_logger():
    """
    Set up and configure the logger
    
    Returns:
        The configured logger instance
    """
    # Get log level from environment
    log_level_str = os.getenv('LOG_LEVEL', 'INFO').upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    
    # Create logs directory if it doesn't exist
    logs_dir = Path(__file__).parent.parent / 'logs'
    logs_dir.mkdir(exist_ok=True)
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # Create formatter
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s', 
                                 datefmt='%Y-%m-%d %H:%M:%S')
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Create file handlers
    error_handler = logging.FileHandler(logs_dir / 'error.log')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)
    
    all_handler = logging.FileHandler(logs_dir / 'combined.log')
    all_handler.setFormatter(formatter)
    logger.addHandler(all_handler)
    
    return logger

def get_logger(name):
    """
    Get a logger instance with the specified name
    
    Args:
        name: Name for the logger
        
    Returns:
        The logger instance
    """
    return logging.getLogger(name)
