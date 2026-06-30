import logging
import logging.config
from pathlib import Path

import streamlit as st
import yaml


def initialize_logs(nom: str):

    logs_dir = Path(__file__).resolve().parents[2] / "logs"
    logs_dir.mkdir(exist_ok=True)

    config_file = Path(__file__).resolve().parents[2] / "logging_config.yml"

    with open(config_file, encoding="utf-8") as stream:
        config = yaml.safe_load(stream)
        logging.config.dictConfig(config)

    logging.info("-" * 50)
    logging.info(f"Launch FRONTEND : {nom}")
    logging.info("-" * 50)


def track_page(page_name: str):
    """
    Tracks the current page in session_state and logs a message
    only when the user navigpates to a new page.
    """
    if "last_navigated_page" not in st.session_state:
        st.session_state.last_navigated_page = None

    if st.session_state.last_navigated_page != page_name:
        logging.info(page_name)
        st.session_state.last_navigated_page = page_name
