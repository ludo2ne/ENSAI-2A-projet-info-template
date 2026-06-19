import logging

import dotenv


def load_environment_variables():
    """Loads environment variables from the .env file."""
    succes = dotenv.load_dotenv(override=True)
    logging.info(f"Load environment variables: {'SUCCES' if succes else 'FAIL'}")


def mask_value(key, value):
    """Masks sensitive values based on their key name.
    Args:
        key (str): The name of the environment variable.
        value (str): The actual value of the environment variable.
    Returns:
        str: A masked string ("*******") if the key contains sensitive
            keywords, otherwise the original value.
    """
    sensitive_keywords = ["PASSWORD", "SECRET", "KEY", "TOKEN"]

    if any(word in key.upper() for word in sensitive_keywords):
        return "*******"
    return value


def display_values():
    """Logs all environment variables."""
    for key, value in dotenv.dotenv_values().items():
        logging.info(f"{key}={mask_value(key, value)}")
