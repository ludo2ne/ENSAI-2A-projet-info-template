"""Implémentation des tests pour la classe Reserve"""

import pytest

from business_object.board import Board
from business_object.carte import Carte
from business_object.main import Main
from business_object.reserve import Reserve
from tests.tests_business_object.test_liste_cartes import AbstractListeCartesTest


class TestReserve(AbstractListeCartesTest):
    @pytest.fixture
    def liste_cartes(self):
        return Reserve([pytest.as_pique, pytest.dix_coeur], False)

    @pytest.fixture
    def cls(self):
        return Reserve

    def test_reserve_init_defaut(self):
        # GIVEN
        resultat = [
            Carte(valeur, couleur) for valeur in Carte.VALEURS() for couleur in Carte.COULEURS()
        ]

        # WHEN
        reserve = Reserve()

        # THEN
        assert reserve.cartes == resultat

    def test_reserve_ajouter_carte_succes(self):
        # GIVEN
        carte = pytest.cinq_trefle
        reserve = Reserve([pytest.as_pique], False)
        resultat = [pytest.as_pique, pytest.cinq_trefle]

        # WHEN
        reserve.ajouter_carte(carte)

        # THEN
        assert reserve.cartes == resultat

    def test_reserve_bruler(self):
        # GIVEN
        reserve = Reserve([pytest.deux_coeur, pytest.huit_coeur, pytest.valet_trefle], False)
        resultat = [pytest.huit_coeur, pytest.valet_trefle, pytest.deux_coeur]

        # WHEN
        reserve.bruler()

        # THEN
        assert reserve.cartes == resultat

    def test_reserve_reveler_succes(self):
        # GIVEN
        reserve = Reserve([pytest.as_pique, pytest.as_trefle, pytest.as_coeur], False)
        board = Board([pytest.roi_pique])
        resultat_reserve = [pytest.as_trefle, pytest.as_coeur]
        resultat_board = [pytest.roi_pique, pytest.as_pique]

        # WHEN
        reserve.reveler(board)

        # THEN
        assert reserve.cartes == resultat_reserve
        assert board.cartes == resultat_board

    def test_reserve_reveler_echec(self):
        # GIVEN
        reserve = Reserve([pytest.as_pique, pytest.as_trefle, pytest.as_coeur], False)
        main = Main(None)
        message_attendu = f"board pas de type Board : {type(main)}"

        # WHEN / THEN
        with pytest.raises(ValueError, match=message_attendu):
            reserve.reveler(main)

    def test_reserve_distribuer_succes(self):
        # GIVEN
        reserve = Reserve(
            [pytest.as_pique, pytest.quatre_trefle, pytest.valet_carreau, pytest.valet_coeur], False
        )
        n_joueurs = 2
        resultat = [
            Main([pytest.as_pique, pytest.valet_carreau]),
            Main([pytest.quatre_trefle, pytest.valet_coeur]),
        ]
        resultat_reserve = []

        # WHEN
        mains = reserve.distribuer(n_joueurs)

        # THEN
        assert mains == resultat
        assert reserve.cartes == resultat_reserve

    def test_reserve_distribuer_echec(self):
        # GIVEN
        reserve = Reserve(
            [pytest.as_pique, pytest.quatre_trefle, pytest.valet_carreau, pytest.valet_coeur], False
        )
        n_joueurs = 3
        message_attendu = (
            f"le nombre de carte dans la reserve est trop petit : {len(reserve.cartes)}"
        )

        # WHEN / THEN
        with pytest.raises(ValueError, match=message_attendu):
            reserve.distribuer(n_joueurs)
