from unittest.mock import patch

from src.service.manche_joueur_service import MancheJoueurService


class Test_MancheJoueurService:
    @patch("src.service.manche_joueur_service.MancheJoueurDAO")
    def test_sauvegarder_manche_joueur_ok(self, MockDAO):
        # GIVEN
        mock_dao = MockDAO.return_value
        mock_dao.creer_manche_joueur.return_value = True
        service = MancheJoueurService()
        service.MancheJoueurDAO = lambda: mock_dao

        # WHEN
        result = service.sauvegarder_manche_joueur(1, "info_manche_mock")

        # THEN
        assert result is True
        mock_dao.creer_manche_joueur.assert_called_once_with(1, "info_manche_mock",{})

    @patch("src.service.manche_joueur_service.MancheJoueurDAO")
    def test_trouver_par_ids_ok(self, MockDAO):
        # GIVEN
        mock_dao = MockDAO.return_value
        expected = [{"id_manche": 1, "id_joueur": 2}]
        mock_dao.trouver_par_ids.return_value = expected
        service = MancheJoueurService()
        service.MancheJoueurDAO = lambda: mock_dao

        # WHEN
        result = service.trouver_par_ids(1, 2)

        # THEN
        assert result == expected
        mock_dao.trouver_par_ids.assert_called_once_with(1, 2)

    @patch("src.service.manche_joueur_service.MancheJoueurDAO")
    def test_supprimer_par_id_manche_ok(self, MockDAO):
        # GIVEN
        mock_dao = MockDAO.return_value
        mock_dao.supprimer_par_id_manche.return_value = True
        service = MancheJoueurService()
        service.MancheJoueurDAO = lambda: mock_dao

        # WHEN
        result = service.supprimer_par_id_manche(1)

        # THEN
        assert result is True
        mock_dao.supprimer_par_id_manche.assert_called_once_with(1)

    @patch("src.service.manche_joueur_service.MancheJoueurDAO")
    def test_supprimer_participation_ok(self, MockDAO):
        # GIVEN
        mock_dao = MockDAO.return_value
        mock_dao.supprimer_participation.return_value = True
        service = MancheJoueurService()
        service.MancheJoueurDAO = lambda: mock_dao

        # WHEN
        result = service.supprimer_participation(1, 2)

        # THEN
        assert result is True
        mock_dao.supprimer_participation.assert_called_once_with(1, 2)
