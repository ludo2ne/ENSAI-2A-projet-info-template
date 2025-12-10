"""Implémentation des tests pour la classe Board"""

import pytest

from business_object.board import Board
from tests.tests_business_object.test_liste_cartes import AbstractListeCartesTest


class TestBoard(AbstractListeCartesTest):
    @pytest.fixture
    def liste_cartes(self):
        return Board([pytest.as_pique, pytest.dix_coeur])

    @pytest.fixture
    def cls(self):
        return Board

    def test_board_init_defaut(self):
        # GIVEN
        resultat = []

        # WHEN
        board = Board()

        # THEN
        assert board.cartes == resultat

    def test_board_init_trop_grand(self, liste_cartes):
        # GIVEN
        cartes = [
            pytest.as_pique,
            pytest.dix_coeur,
            pytest.as_pique,
            pytest.dix_coeur,
            pytest.as_pique,
            pytest.dix_coeur,
        ]
        message_attendu = f"Le nombre de cartes dans le board est trop grand : {len(cartes)}"

        # WHEN / THEN
        with pytest.raises(ValueError, match=message_attendu):
            Board(cartes)

    def test_board_ajouter_carte_succes(self):
        # GIVEN
        carte = pytest.cinq_trefle
        board = Board([pytest.as_pique])
        resultat = [pytest.as_pique, pytest.cinq_trefle]

        # WHEN
        board.ajouter_carte(carte)

        # THEN
        assert board.cartes == resultat

    def test_board_ajouter_cartes_echec(self):
        # GIVEN
        board = Board(
            [pytest.as_pique, pytest.dix_coeur, pytest.as_pique, pytest.dix_coeur, pytest.as_pique]
        )
        carte = pytest.as_coeur
        message_attendu = (
            f"Le nombre de cartes dans le board est trop grand : {len(board.cartes) + 1}"
        )

        # WHEN / THEN
        with pytest.raises(ValueError, match=message_attendu):
            board.ajouter_carte(carte)

    @pytest.mark.parametrize(
        "cartes, resultat",
        [
            (None, "   [?]      [?]      [?]      [?]      [?]   "),
            (
                [pytest.deux_pique, pytest.dix_pique, pytest.valet_coeur],
                "  2 de pique    10 de pique    Valet de coeur     [?]      [?]   ",
            ),
            (
                [
                    pytest.deux_pique,
                    pytest.dix_pique,
                    pytest.valet_coeur,
                    pytest.as_trefle,
                    pytest.quatre_carreau,
                ],
                "  2 de pique    10 de pique    Valet de coeur    As de trêfle    4 de carreau  ",
            ),
        ],
    )
    def test_affichage_board(self, cartes, resultat):
        # GIVEN
        board = Board(cartes)

        # WHEN
        affichage = board.affichage_board()

        # THEN
        assert affichage == resultat
