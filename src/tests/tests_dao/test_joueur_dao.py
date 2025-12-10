"""Implémentation des tests pour la classe JoueurDA"""

from business_object.joueur import Joueur
from dao.joueur_dao import JoueurDao
from utils.reset_database import ResetDatabase


class TestJoueurDao:
    def test_creer_succes(self):
        if ResetDatabase().lancer(True):
            # GIVEN
            pseudo = "paul"
            pays = "fr"
            joueurDao = JoueurDao()

            # WHEN
            resultat = joueurDao.creer(pseudo, pays)

            # THEN
            assert resultat is True

    def test_creer_echec(self):
        if ResetDatabase().lancer(True):
            # GIVEN
            pseudo = "paul"
            pays = "fr"
            joueurDao = JoueurDao()

            # WHEN
            resultat1 = joueurDao.creer(pseudo, pays)
            resultat2 = joueurDao.creer(pseudo, pays)

            # THEN
            assert resultat1 is True
            assert resultat2 is False

    def test_trouver_par_id_succes(self):
        if ResetDatabase().lancer(True):
            # GIVEN
            joueurDao = JoueurDao()
            id_joueur = 999
            joueur_recherche = Joueur(999, "admin", 0, "fr")

            # WHEN
            resultat = joueurDao.trouver_par_id(id_joueur)

            # THEN
            assert resultat == joueur_recherche

    def test_trouver_par_id_echec(self):
        if ResetDatabase().lancer(True):
            # GIVEN
            joueurDao = JoueurDao()
            id_joueur = 1

            # WHEN
            resultat = joueurDao.trouver_par_id(id_joueur)

            # THEN
            assert resultat is None

    def test_lister_tous(self):
        if ResetDatabase().lancer(True):
            # GIVEN
            joueurDao = JoueurDao()
            liste = (
                "[admin : 0 crédits, a : 20 crédits, maurice : 20 crédits, batricia : 25 crédits]"
            )

            # WHEN
            resultat = joueurDao.lister_tous()

            # THEN
            assert resultat == liste

    def test_modifier_succes(self):
        if ResetDatabase().lancer(True):
            # GIVEN
            joueurDao = JoueurDao()
            joueur2 = Joueur(999, "admin", 50, "fr")

            # WHEN
            resultat = joueurDao.modifier(joueur2)

            # THEN
            assert resultat is True
            assert joueurDao.trouver_par_id(999) == joueur2

    def test_modifier_echec(self):
        if ResetDatabase().lancer(True):
            # GIVEN
            joueurDao = JoueurDao()
            joueur2 = Joueur(1, "admin", 50, "fr")

            # WHEN
            resultat = joueurDao.modifier(joueur2)

            # THEN
            assert resultat is False
            assert joueurDao.trouver_par_id(999) != joueur2

    def test_supprimer_succes(self):
        if ResetDatabase().lancer(True):
            # GIVEN
            joueurDao = JoueurDao()
            joueur = Joueur(999, "admin", 50, "fr")

            # WHEN
            resultat = joueurDao.supprimer(joueur)

            # THEN
            assert resultat is True
            assert joueurDao.trouver_par_id(999) is None

    def test_supprimer_echec(self):
        if ResetDatabase().lancer(True):
            # GIVEN
            joueurDao = JoueurDao()
            joueur = Joueur(1, "admin", 50, "fr")

            # WHEN
            resultat = joueurDao.supprimer(joueur)

            # THEN
            assert resultat is False
            assert joueurDao.trouver_par_id(1) is None

    def test_connection_succes(self):
        if ResetDatabase().lancer(True):
            # GIVEN
            joueurDao = JoueurDao()
            joueur = Joueur(999, "admin", 50, "fr")
            pseudo = "admin"

            # WHEN
            resultat = joueurDao.se_connecter(pseudo)

            # THEN
            assert resultat == joueur
