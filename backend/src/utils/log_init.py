import logging
import logging.config
from pathlib import Path

import yaml


def initialize_logs(name: str):
    """Initialize logging from a configuration file"""

    # Create the logs folder at project root if it doesn't exist
    logs_dir = Path(__file__).resolve().parents[2] / "logs"
    logs_dir.mkdir(exist_ok=True)

    config_file = Path(__file__).resolve().parents[2] / "logging_config.yml"

    with open(config_file, encoding="utf-8") as stream:
        config = yaml.safe_load(stream)
        logging.config.dictConfig(config)

        logging.info("-" * 50)
        logging.info(f"Starting {name}                           ")
        logging.info("-" * 50)
