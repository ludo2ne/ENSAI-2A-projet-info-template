"""Implémentation de la classe CreditService"""

import logging

from business_object.joueur import Joueur
from dao.joueur_dao import JoueurDao
from service.joueur_service import JoueurService
from utils.log_decorator import log

logger = logging.getLogger(__name__)


class CreditService:
    """Service de gestion des crédits des joueurs"""

    @log
    def crediter(self, joueur: Joueur, montant: int) -> None:
        """
        Crédite un joueur dans la RAM et dans la DAO

        Paramètres
        ----------
        id_joueur : int
            l'identifiant du jouur qui est débité

        Renvois
        -------
        None

        Exceptions
        ----------
        ValueError
            si le montant à créditer est incorrect

        """

        ram_modif = False

        try:
            joueur.ajouter_credits(montant)
            ram_modif = True
            JoueurDao().modifier(joueur)
        except Exception as e:
            if ram_modif:
                joueur.retirer_credits(montant)

            logger.error(f"Échec du crédit pour {joueur.pseudo} : {e}")
            raise Exception(f"Échec du crédit pour {joueur.pseudo} : {e}")

        if joueur.id_joueur in JoueurService()._joueurs_connectes.keys():
            JoueurService().maj_joueur(joueur)

    @log
    def debiter(self, id_joueur: int, montant: int) -> str:
        """
        Crédite un joueur dans la RAM et dans la DAO

        Paramètres
        ----------
        id_joueur : int
            l'identifiant du jouur qui est débité

        Renvois
        -------
        None

        Exceptions
        ----------
        ValueError
            si le montant à créditer est incorrect


        joueur = self.joueur_par_id(id_joueur)
        """

        if id_joueur in JoueurService()._joueurs_connectes.keys():
            joueur = JoueurService().trouver_par_id(id_joueur)

            ram_modif = False

            try:
                joueur.retirer_credits(montant)
                ram_modif = True
                JoueurDao().modifier(joueur)
            except Exception as e:
                if ram_modif:
                    joueur.ajouter_credits(montant)

                logger.error(f"Échec du débit pour {joueur.pseudo} : {e}")
                raise Exception(f"Échec du crédit pour {joueur.pseudo} : {e}")

            message = f"Le joueur {joueur.pseudo} a été débité de {montant} avec succès"

        else:
            joueur = JoueurDao().trouver_par_id(id_joueur)
            joueur.retirer_credits(montant)
            JoueurDao().modifier(joueur)

            message = f"Le joueur {joueur.pseudo} a été débité de {montant} avec succès"

        return message
