import logging
from pathlib import Path

import dotenv


def load_environment_variables():
    succes = dotenv.load_dotenv(
        dotenv_path=Path(__file__).resolve().parents[2] / ".env", override=True
    )
    logging.info(f"Load environment variables: {'SUCCES' if succes else 'FAIL'}")


def mask_value(key, value):
    """Mask sensitive values"""
    sensitive_keywords = ["PASSWORD", "SECRET", "KEY", "TOKEN"]

    if any(word in key.upper() for word in sensitive_keywords):
        return "*******"
    return value


def display_values():
    for key, value in dotenv.dotenv_values().items():
        logging.info(f"{key}={mask_value(key, value)}")
