import logging
import logging.config
import os

import yaml


def initialiser_logs(nom):
    """Initialiser les logs à partir du fichier de config"""

    # print current working directory
    # print(os.getcwd())
    # os.chdir('ENSAI-2A-projet-info-template')

    # Création du dossier logs à la racine si non existant
    os.makedirs("logs", exist_ok=True)

    with open("logging_config.yml", encoding="utf-8") as stream:
        config = yaml.safe_load(stream)

    logging.config.dictConfig(config)

    logging.info("-" * 50)
    logging.info(f"Lancement {nom}                           ")
    logging.info("-" * 50)
