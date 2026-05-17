"""
Test Data — Shared data loader for test scenarios.
Loads from data/ directory (JSON/CSV files).
"""
import json
from pathlib import Path
from config.env_config import DATA_DIR
from utils.logger import get_logger

logger = get_logger(__name__)


def load_json_data(filename: str) -> dict:
    """Load test data from a JSON file in data/ directory.
    
    Args:
        filename: JSON filename (e.g., 'login_credentials.json')
    """
    filepath = DATA_DIR / filename
    if not filepath.exists():
        logger.error(f"Test data file not found: {filepath}")
        raise FileNotFoundError(f"Missing test data: {filepath}")
    
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)


def get_test_credentials(user_type: str = "valid") -> dict:
    """Get credentials by user type from login test data.
    
    Args:
        user_type: 'valid', 'invalid', 'locked', 'expired'
    """
    data = load_json_data("credentials.json")
    if user_type not in data:
        raise KeyError(f"Unknown user_type '{user_type}'. Available: {list(data.keys())}")
    return data[user_type]
