from unittest.mock import Mock, patch

import pytest

from business_object.info_manche import InfoManche
from business_object.joueur import Joueur
from business_object.manche import Manche
from src.service.action_service import ActionService


class Test_Action_Service:
    def test_manche_joueur(self):
        # GIVEN
        joueur1 = Joueur(1, "A", 100, "France")
        joueur2 = Joueur(2, "B", 100, "France")
        ids_joueurs = [joueur1.id_joueur, joueur2.id_joueur]
        info = InfoManche(joueurs=ids_joueurs)

        manche = Manche(info=info, grosse_blind=50)
        table = type("Table", (), {"manche": manche, "numero_table": 1})()

        joueur1._Joueur__table = table
        joueur1.numero_table = 1
        
        service = ActionService()

        with patch("src.service.action_service.JoueurService") as MockJS, \
             patch("src.service.action_service.TableService") as MockTS:
            
            instance_js = MockJS.return_value
            instance_js.trouver_par_id.return_value = joueur1
            instance_ts = MockTS.return_value
            instance_ts.table_par_numero.return_value = table

            # WHEN
            result = service.manche_joueur(joueur1.id_joueur)

            # THEN
            assert result == manche

    def test_manche_joueur_table_sans_manche(self):
        # GIVEN
        joueur1 = Joueur(1, "A", 100, "France")
        table = type("Table", (), {"manche": None, "numero_table": 1})()
        # WHEN
        joueur1._Joueur__table = table
        joueur1.numero_table = 1

        service = ActionService()
        with patch("src.service.action_service.JoueurService") as MockJS, \
             patch("src.service.action_service.TableService") as MockTS:
            instance_js = MockJS.return_value
            instance_js.trouver_par_id.return_value = joueur1
            instance_ts = MockTS.return_value
            instance_ts.table_par_numero.return_value = table

            # THEN
            with pytest.raises(ValueError, match="aucune manche n'est en cours"):
                service.manche_joueur(joueur1.id_joueur)

    def test_manche_joueur_pas_dans_manche(self):
        # GIVEN
        joueur1 = Joueur(1, "A", 100, "France")
        joueur2 = Joueur(2, "B", 100, "France")
        joueur3 = Joueur(3, "C", 100, "France")
        # WHEN
        info = InfoManche(joueurs=[joueur2.id_joueur, joueur3.id_joueur])
        manche = Manche(info=info, grosse_blind=50)
        table = type("Table", (), {"manche": manche, "numero_table": 1})()
        joueur1._Joueur__table = table
        joueur1.numero_table = 1
        service = ActionService()
        # THEN
        with patch("src.service.action_service.JoueurService") as MockJS, \
             patch("src.service.action_service.TableService") as MockTS:

            instance_js = MockJS.return_value
            instance_js.trouver_par_id.return_value = joueur1
            instance_ts = MockTS.return_value
            instance_ts.table_par_numero.return_value = table

            service.joueur_par_id = lambda _id: joueur1

            with pytest.raises(ValueError, match="ne participe pas à la manche"):
                service.manche_joueur(joueur1.id_joueur)

    def test_manche_all_in_pas_tour(self):
        # GIVEN
        joueur = Mock()
        joueur.pseudo = "A"

        manche = Mock()
        manche.est_tour.return_value = False
        manche.indice_joueur.return_value = 0

        info_mock = Mock()
        info_mock.all_in.return_value = 100
        manche.info = info_mock

        service = ActionService()
        service.manche_joueur = Mock(return_value=manche)

        with (
            patch("src.service.action_service.JoueurService") as MockJoueurService,
            patch("src.service.action_service.CreditService") as MockCreditService,
        ):
            MockJoueurService.return_value.trouver_par_id.return_value = joueur

            instance_credit = MockCreditService.return_value
            instance_credit.debiter = Mock()

            # WHEN 
            with pytest.raises(Exception):
                service.all_in(id_joueur=1)

            instance_credit.debiter.assert_not_called()

    def test_se_coucher_ok(self):
        # GIVEN
        joueur = Mock()
        joueur.pseudo = "A"

        manche = Mock()
        manche.est_tour.return_value = True
        manche.indice_joueur.return_value = 0
        manche.info = Mock()  
        manche.action = Mock(side_effect=lambda id_joueur, action: manche.info.coucher_joueur(0, 3) 
                                        if action=="se coucher" else None)

        service = ActionService()
        service.manche_joueur = Mock(return_value=manche)

        with patch("src.service.action_service.JoueurService") as MockJoueurService:
            MockJoueurService.return_value.trouver_par_id.return_value = joueur

            # WHEN
            service.se_coucher(id_joueur=1)

            # THEN
            manche.info.coucher_joueur.assert_called_once_with(0, 3)

    def test_checker_ok(self):
        # GIVEN
        joueur = Mock()
        joueur.pseudo = "A"

        manche = Mock()
        service = ActionService()
        service.manche_joueur = Mock(return_value=manche)

        with patch("src.service.action_service.JoueurService") as MockJoueurService:
            MockJoueurService.return_value.trouver_par_id.return_value = joueur

            # WHEN
            service.checker(id_joueur=1)

            # THEN
            manche.action.assert_called_once_with(1, "checker")


    def test_checker_statut_incorrect(self):
        # GIVEN
        joueur = Mock()
        joueur.pseudo = "A"

        manche = Mock()
        manche.est_tour.return_value = True
        manche.indice_joueur.return_value = 0

        # On simule que checker est interdit
        info_mock = Mock()
        manche.info = info_mock
        manche.action = Mock(side_effect=lambda id_joueur, action: (_ for _ in ()).throw(ValueError(f"{joueur.pseudo} ne peut pas checker")) if action=="checker" else None)

        service = ActionService()
        service.manche_joueur = Mock(return_value=manche)

        with patch("src.service.action_service.JoueurService") as MockJoueurService:
            MockJoueurService.return_value.trouver_par_id.return_value = joueur

            # WHEN / THEN
            with pytest.raises(ValueError, match=f"{joueur.pseudo} ne peut pas checker"):
                service.checker(id_joueur=1)

    def test_suivre_ok(self):
        # GIVEN
        joueur = Mock()
        joueur.pseudo = "A"
        joueur.credit = 100

        manche = Mock()
        manche.est_tour.return_value = True
        manche.action = Mock(return_value=50)  

        service = ActionService()
        service.manche_joueur = Mock(return_value=manche)

        with (
            patch("src.service.action_service.JoueurService") as MockJoueurService,
            patch("src.service.action_service.CreditService") as MockCreditService,
        ):
            MockJoueurService.return_value.trouver_par_id.return_value = joueur
            instance_credit = MockCreditService.return_value
            instance_credit.debiter = Mock()

            # WHEN
            service.suivre(id_joueur=1)

            # THEN
            manche.action.assert_called_once_with(1, "suivre", joueur.credit, 0)
            instance_credit.debiter.assert_called_once_with(1, 50)
