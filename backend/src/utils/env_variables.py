import logging

import dotenv


def load_environment_variables():
    dotenv.load_dotenv(override=True)


def mask_value(key, value):
    """Mask sensitive values"""
    sensitive_keywords = ["PASSWORD", "SECRET", "KEY", "TOKEN"]

    if any(word in key.upper() for word in sensitive_keywords):
        return "*******"
    return value


def display_values():
    for key, value in dotenv.dotenv_values().items():
        logging.info(f"{key}={mask_value(key, value)}")
