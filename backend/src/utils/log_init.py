import logging
import logging.config
from pathlib import Path

import yaml


def initialiser_logs(nom):
    """Initialiser les logs à partir du fichier de config"""

    # print current working directory
    # print(os.getcwd())
    # os.chdir('ENSAI-2A-projet-info-template')

    # Création du dossier logs à la racine si non existant
    logs_dir = Path(__file__).resolve().parents[4] / "logs"
    logs_dir.mkdir(exist_ok=True)

    config_file = Path(__file__).resolve().parents[2] / "logging_config.yml"

    with open(config_file, encoding="utf-8") as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)
        logging.config.dictConfig(config)

        logging.info("-" * 50)
        logging.info(f"Lancement {nom}                           ")
        logging.info("-" * 50)
