"""Implémenation des tests de la classe MancheJoueurDAO"""

from unittest.mock import MagicMock, patch

import pytest

from business_object.info_manche import InfoManche
from business_object.main import Main
from business_object.joueur import Joueur
from dao.manche_joueur_dao import MancheJoueurDAO


class TestMancheJoueurDAO:
    @pytest.fixture
    def setup_data(self):
        dao = MancheJoueurDAO()

        j1 = 1
        j2 = 2

        info = InfoManche([j1, j2],)
        info.modifier_mise(0, 100)
        info.assignation_mains([Main([pytest.trois_carreau, pytest.quatre_carreau]), Main([pytest.as_carreau, pytest.roi_carreau])])
        info.modifier_tour_couche(1, 2)

        return dao, info


    @patch("dao.manche_joueur_dao.DBConnection")
    def test_creer_manche_joueur_succes(self, mock_db, setup_data):
        dao, info_manche = setup_data

        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_db.return_value.connection.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        result = dao.creer_manche_joueur(1, info_manche,{})

        assert result is True
        assert mock_cursor.execute.call_count == 2

    @patch("dao.manche_joueur_dao.DBConnection")
    def test_creer_manche_joueur_exception(self, mock_db, setup_data):
        dao, info_manche = setup_data

        mock_db.return_value.connection.__enter__.side_effect = Exception("DB error")

        result = dao.creer_manche_joueur(1, info_manche)

        assert result is False

    @patch("dao.manche_joueur_dao.DBConnection")
    def test_trouver_par_ids(self, mock_db, setup_data):
        dao, _ = setup_data

        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_cursor.fetchall.return_value = [
            {
                "id_manche": 1,
                "id_joueur": 1,
                "carte_main_1": "As de pique",
                "carte_main_2": "Roi de coeur",
                "gain": 200,
                "mise": 100,
                "tour_couche": None,
            }
        ]

        mock_db.return_value.connection.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        result = dao.trouver_par_ids(997, 997)

        assert len(result) == 1
        assert result[0]["id_joueur"] == 1
        mock_cursor.execute.assert_called_once()

    @patch("dao.manche_joueur_dao.DBConnection")
    def test_supprimer_par_id_manche(self, mock_db, setup_data):
        dao, _ = setup_data

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 2

        mock_db.return_value.connection.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        result = dao.supprimer_par_id_manche(1)

        assert result is True
        mock_cursor.execute.assert_called_once()

    @patch("dao.manche_joueur_dao.DBConnection")
    def test_supprimer_participation(self, mock_db, setup_data):
        dao, _ = setup_data

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1

        mock_db.return_value.connection.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        result = dao.supprimer_participation(1, 2)

        assert result is True
        mock_cursor.execute.assert_called_once()
