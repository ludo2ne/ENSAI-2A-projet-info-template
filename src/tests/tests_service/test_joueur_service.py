from unittest.mock import patch

from business_object.joueur import Joueur
from src.service.joueur_service import JoueurService


class Test_JoueurService:
    @patch("src.service.joueur_service.JoueurDao")
    def test_joueur_service_se_connecter_ok(self, MockDao):
        # GIVEN
        mock_dao = MockDao.return_value
        joueur = Joueur(1, "A", 2000, "France")
        mock_dao.se_connecter.return_value = joueur
        service = JoueurService()
        service.dao = mock_dao

        # WHEN
        result = service.se_connecter("A")

        # THEN
        assert result == joueur
        mock_dao.se_connecter.assert_called_once_with("A")

    @patch("src.service.joueur_service.JoueurDao")
    def test_joueur_service_pseudo_deja_utilise_vrai(self, MockDao):
        # GIVEN
        mock_dao = MockDao.return_value
        mock_dao.se_connecter.return_value = Joueur(1, "A", 2000, "France")
        service = JoueurService()
        service.dao = mock_dao

        # WHEN
        result = service.pseudo_deja_utilise("A")

        # THEN
        assert result is True

    @patch("src.service.joueur_service.JoueurDao")
    def test_joueur_service_pseudo_deja_utilise_faux(self, MockDao):
        # GIVEN
        mock_dao = MockDao.return_value
        mock_dao.se_connecter.return_value = None
        service = JoueurService()
        service.dao = mock_dao

        # WHEN
        result = service.pseudo_deja_utilise("B")

        # THEN
        assert result is False

    @patch("src.service.joueur_service.JoueurDao")
    def test_joueur_service_creer_ok(self, MockDao):
        # GIVEN
        mock_dao = MockDao.return_value
        joueur_cree = Joueur(1, "A", 2000, "France")
        mock_dao.se_connecter.side_effect = [None, joueur_cree]
        mock_dao.creer.return_value = True
        service = JoueurService()
        service.dao = mock_dao

        # WHEN
        joueur = service.creer("A", "France")

        # THEN
        assert joueur == joueur_cree
        mock_dao.creer.assert_called_once_with("A", "France")
        assert mock_dao.se_connecter.call_count == 2

    @patch("src.service.joueur_service.JoueurDao")
    def test_joueur_service_creer_deja_utilise(self, MockDao):
        # GIVEN
        mock_dao = MockDao.return_value
        mock_dao.se_connecter.return_value = Joueur(1, "A", 2000, "France")
        service = JoueurService()
        service.dao = mock_dao

        # WHEN
        joueur = service.creer("A", "France")

        # THEN
        assert joueur is None
        mock_dao.creer.assert_not_called()

    @patch("src.service.joueur_service.JoueurDao")
    def test_joueur_service_trouver_par_id(self, MockDao):
        # GIVEN
        mock_dao = MockDao.return_value
        joueur = Joueur(1, "A", 2000, "France")
        mock_dao.trouver_par_id.return_value = joueur

        service = JoueurService()
        service.dao = mock_dao

        # Simuler que le joueur est connecté
        service._joueurs_connectes[joueur.id_joueur] = joueur

        # WHEN
        result = service.trouver_par_id(1)

        # THEN
        assert result == joueur

    @patch("src.service.joueur_service.JoueurDao")
    def test_joueur_service_trouver_par_pseudo(self, MockDao):
        # GIVEN
        mock_dao = MockDao.return_value
        joueur = Joueur(1, "A", 2000, "France")
        mock_dao.trouver_par_pseudo.return_value = joueur
        service = JoueurService()
        service.dao = mock_dao

        # WHEN
        result = service.trouver_par_pseudo("A")

        # THEN
        assert result == joueur
        mock_dao.trouver_par_pseudo.assert_called_once_with("A")

    @patch("src.service.joueur_service.JoueurDao")
    def test_joueur_service_lister_tous(self, MockDao):
        # GIVEN
        mock_dao = MockDao.return_value
        joueurs = [Joueur(1, "A", 2000, "France"), Joueur(2, "B", 2000, "France")]
        mock_dao.lister_tous.return_value = joueurs
        service = JoueurService()
        service.dao = mock_dao

        # WHEN
        result = service.lister_tous()

        # THEN
        assert result == joueurs
        mock_dao.lister_tous.assert_called_once()

    @patch("src.service.joueur_service.JoueurDao")
    def test_joueur_service_modifier_ok(self, MockDao):
        # GIVEN
        mock_dao = MockDao.return_value
        joueur = Joueur(1, "A", 2000, "France")
        mock_dao.modifier.return_value = True
        service = JoueurService()
        service.dao = mock_dao

        # WHEN
        result = service.modifier(joueur)

        # THEN
        assert result == joueur
        mock_dao.modifier.assert_called_once_with(joueur)

    @patch("src.service.joueur_service.JoueurDao")
    def test_joueur_service_modifier_fail(self, MockDao):
        # GIVEN
        mock_dao = MockDao.return_value
        joueur = Joueur(1, "A", 2000, "France")
        mock_dao.modifier.return_value = False
        service = JoueurService()
        service.dao = mock_dao

        # WHEN
        result = service.modifier(joueur)

        # THEN
        assert result is None
        mock_dao.modifier.assert_called_once_with(joueur)

    @patch("src.service.joueur_service.JoueurDao")
    def test_joueur_service_supprimer_ok(self, MockDao):
        # GIVEN
        mock_dao = MockDao.return_value
        joueur = Joueur(1, "A", 2000, "France")
        mock_dao.supprimer.return_value = True
        service = JoueurService()
        service.dao = mock_dao

        # WHEN
        result = service.supprimer(joueur)

        # THEN
        assert result is True
        mock_dao.supprimer.assert_called_once_with(joueur)

    @patch("src.service.joueur_service.JoueurDao")
    def test_joueur_service_supprimer_fail(self, MockDao):
        # GIVEN
        mock_dao = MockDao.return_value
        joueur = Joueur(1, "A", 2000, "France")
        mock_dao.supprimer.return_value = False
        service = JoueurService()
        service.dao = mock_dao

        # WHEN
        result = service.supprimer(joueur)

        # THEN
        assert result is False
        mock_dao.supprimer.assert_called_once_with(joueur)
