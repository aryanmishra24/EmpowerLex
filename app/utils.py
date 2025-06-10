import uuid
import logging
from datetime import datetime
from typing import Any, Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_uuid() -> str:
    """Generate a unique UUID string"""
    return str(uuid.uuid4())

def log_info(message: str, extra_data: Dict[str, Any] = None):
    """Log information with optional extra data"""
    if extra_data:
        logger.info(f"{message} - Extra: {extra_data}")
    else:
        logger.info(message)

def log_error(message: str, error: Exception = None):
    """Log error with optional exception details"""
    if error:
        logger.error(f"{message} - Error: {str(error)}")
    else:
        logger.error(message)

def format_datetime(dt: datetime) -> str:
    """Format datetime for API responses"""
    return dt.isoformat()
