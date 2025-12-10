"""Implémentation des tests pour la classe MancheDAO"""

from business_object.info_manche import InfoManche
from business_object.joueur import Joueur
from business_object.manche import Manche
from dao.manche_dao import MancheDao
from utils.reset_database import ResetDatabase


class TestMancheDao:
    def creer_manche(self):
        # Crée une instance de Manche prête à être utilisée
        joueur1 = 1
        joueur2 = 2
        info = InfoManche([joueur1, joueur2])
        manche = Manche(info, 10)
        manche.preflop()
        manche.flop()
        manche.turn()
        manche.river()
        return manche

    def test_sauvegarder_succes(self):
        if ResetDatabase().lancer(True):
            # GIVEN
            mancheDao = MancheDao()
            manche = self.creer_manche()

            # WHEN
            resultat = mancheDao.sauvegarder(manche)

            # THEN
            assert resultat > 0

    def test_sauvegarder_echec(self):
        if ResetDatabase().lancer(True):
            # GIVEN
            mancheDao = MancheDao()
            joueur1 = 1
            joueur2 = 2
            info = InfoManche([joueur1, joueur2])
            manche = Manche(info, 10)
            manche.preflop()
            # on ne va PAS jusqu’à river -> cartes incomplètes

            # WHEN
            resultat = mancheDao.sauvegarder(manche)

            # THEN
            assert resultat is None

    def test_supprimer_succes(self):
        if ResetDatabase().lancer(True):
            # GIVEN
            mancheDao = MancheDao()
            manche = self.creer_manche()
            mancheDao.sauvegarder(manche)

            # WHEN
            resultat = mancheDao.supprimer(manche)

            # THEN
            assert resultat is True

    def test_supprimer_echec(self):
        if ResetDatabase().lancer(True):
            # GIVEN
            mancheDao = MancheDao()
            manche = self.creer_manche()

            # WHEN
            resultat = mancheDao.supprimer(manche)

            # THEN
            assert resultat is False
