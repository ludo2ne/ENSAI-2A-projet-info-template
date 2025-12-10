import logging
import time
from abc import ABC, abstractmethod


class VueAbstraite(ABC):
    """Modèle de Vue"""

    def __init__(self, message: str = "", temps_attente: int = 0, input_attente: bool = False):
        self.message = message
        self.temps_attente = temps_attente
        self.input_attente = input_attente
        logging.info(type(self).__name__)

    def nettoyer_console(self):
        """Insérer des lignes vides pour simuler un nettoyage"""
        for _ in range(30):
            print("")

    def afficher(self) -> None:
        """Echappe un grand espace dans le terminal pour simuler
        le changement de page de l'application"""
        self.nettoyer_console()
        print(self.message)

        print()

        time.sleep(self.temps_attente)

        if self.input_attente:
            input("Appuyez sur entrée pour continuer...")

    @abstractmethod
    def choisir_menu(self):
        """Choix du menu suivant de l'utilisateur"""
        pass
