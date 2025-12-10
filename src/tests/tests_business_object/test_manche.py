import pytest

from business_object.board import Board
from business_object.carte import Carte
from business_object.info_manche import InfoManche
from business_object.main import Main
from business_object.manche import Manche


class Test_Manche:
    # GIVEN/ WHEN
    @pytest.fixture
    @staticmethod
    def joueurs():
        return [1, 2, 3]

    @pytest.fixture
    @staticmethod
    def info_manche(joueurs):
        return InfoManche(joueurs)

    @pytest.fixture
    @staticmethod
    def manche(info_manche):
        m = Manche(info_manche, grosse_blind=10)
        m._Manche__indice_joueur_actuel = 0
        # Assigner des mains valides
        mains = [
            Main(cartes=[Carte("2", "Trêfle"), Carte("3", "Trêfle")]),
            Main(cartes=[Carte("4", "Trêfle"), Carte("5", "Trêfle")]),
            Main(cartes=[Carte("6", "Trêfle"), Carte("7", "Trêfle")]),
        ]
        m.info.assignation_mains(mains)

        # Ajouter board complet
        m._board = Board(
            cartes=[
                Carte("10", "Pique"),
                Carte("Valet", "Pique"),
                Carte("Dame", "Pique"),
                Carte("Roi", "Pique"),
                Carte("As", "Pique"),
            ]
        )

        m.tour = 3
        return m

    @staticmethod
    def remplir_board(manche):
        manche.board.cartes.clear()
        for carte in [
            Carte("2", "Pique"),
            Carte("5", "Trêfle"),
            Carte("8", "Carreau"),
            Carte("10", "Trêfle"),
            Carte("Roi", "Carreau"),
        ]:
            manche.board.ajouter_carte(carte)
        manche.tour = 3

    def test_manche_init(self, manche, info_manche):
        # THEN
        assert manche.tour == 3
        assert manche.info == info_manche
        assert manche.indice_joueur_actuel == 0
        assert manche.grosse_blind == 10
        assert manche.fin is False
        assert manche.board is not None
        assert manche.reserve is not None

    def test_manche_indice_joueur(self, manche, joueurs):
        # THEN
        assert manche.indice_joueur(joueurs[0]) == 0

    def test_manche_indice_joueur_inexistant(self, manche):
        # GIVEN/WHEN
        joueur_inexistant = -1
        # THEN
        with pytest.raises(ValueError):
            manche.indice_joueur(joueur_inexistant)

    def test_manche_regarder_cartes(self, manche):
        # GIVEN
        joueur = manche.info.joueurs[1]
        resultat = "  4 de trêfle    5 de trêfle  "

        # WHEN
        affichage = manche.regarder_cartes(joueur)

        # THEN
        assert resultat == affichage

    def test_manche_est_tour(self, manche, joueurs):
        # GIVEN/WHEN
        j0, j1, j2 = joueurs
        # THEN
        assert manche.est_tour(j0) is True
        assert manche.est_tour(j1) is False
        assert manche.est_tour(j2) is False

    def test_manche_indice_joueur_suivant(self, manche):
        # GIVEN
        # WHEN
        # THEN
        assert manche.indice_joueur_suivant() == 1

    def test_manche_checker(self, manche):
        # GIVEN/WHEN
        manche.info.statuts[:] = [0, 0, 0]
        manche.checker(0)
        # THEN
        assert manche.info.statuts[0] == 2

        # THEN
        with pytest.raises(TypeError):
            manche.checker("0")
        # THEN
        with pytest.raises(ValueError):
            manche.checker(0)

    def test_manche_suivre_relance(self, manche):
        # GIVEN/WHEN
        montant = manche.suivre(0, 500, relance=10)
        # HEN
        assert montant > 0
        assert manche.info.mises[0] > 0
        assert manche.info.statuts[0] == 2

    def test_manche_se_coucher(self, manche):
        # GIVEN/WHEN
        manche.se_coucher(0)
        # THEN
        assert manche.info.statuts[0] == 3
        assert manche.info.tour_couche[0] == manche.tour

    def test_manche_all_in(self, manche):
        # GIVEN/WHEN
        credit = 200
        montant = manche.all_in(0, credit)
        # THEN
        assert montant == credit
        assert manche.info.statuts[0] == 4

    def test_manche_fin_du_tour(self, manche):
        # GIVEN/WHEN
        manche.info.statuts[:] = [2, 2, 2]
        # THEN
        assert manche.fin_du_tour() is True

    def test_manche_fin_de_manche(self, manche):
        # GIVEN/WHEN
        manche.info.statuts[:] = [2, 3, 2]
        # THEN
        assert manche.fin_de_manche() is True

    def test_manche_valeur_pot(self, manche):
        # GIVEN/WHEN
        manche.info.mises[:] = [10, 20, 30]
        # THEN
        assert manche.valeur_pot() == 60

    def test_manche_joueurs_en_lice(self, manche):
        # GIVEN/WHEN
        manche.info.statuts[:] = [0, 3, 0]
        joueurs = manche.joueurs_en_lice
        # THEN
        assert len(joueurs) == 2

    def test_manche_classement_erreur_board_incomplete(self, manche):
        # GIVEN/WHEN
        manche._tour = 2
        # THEN
        with pytest.raises(ValueError):
            manche.classement()

    def test_manche_classement_simple(self, manche):
        # GIVEN
        Test_Manche.remplir_board(manche)

        manche.info.mains[0]._cartes = [Carte("2", "Trêfle"), Carte("3", "Carreau")]
        manche.info.mains[1]._cartes = [Carte("4", "Trêfle"), Carte("6", "Carreau")]
        manche.info.mains[2]._cartes = [Carte("7", "Trêfle"), Carte("9", "Carreau")]
        # WHEN
        classement = manche.classement()
        # THEN
        assert sorted(classement) == [1, 2, 3]

    def test_manche_classement_ex_aequo(self, manche):
        # GIVEN
        Test_Manche.remplir_board(manche)

        manche.info.mains[0]._cartes = [Carte("2", "Trêfle"), Carte("3", "Carreau")]
        manche.info.mains[1]._cartes = [Carte("2", "Trêfle"), Carte("3", "Carreau")]
        manche.info.mains[2]._cartes = [Carte("4", "Trêfle"), Carte("5", "Carreau")]
        # WHEN
        classement = manche.classement()
        # THEN
        assert classement[2] != classement[0]

    def test_manche_recuperer_montant_superieur(self, manche):
        # GIVEN/WHEN/THEN
        assert manche.recuperer(50, 100) == [0, 50]

    def test_manche_recuperer_montant_inferieur(self, manche):
        # GIVEN/WHEN/THEN
        assert manche.recuperer(50, 20) == [30, 20]

    def test_manche_recuperer_montant_egal(self, manche):
        # GIVEN/WHEN/THEN
        assert manche.recuperer(50, 50) == [0, 50]

    def test_manche_gains_un_seul_joueur(self, manche):
        # GIVEN
        manche.info.statuts[:] = [2, 3, 3]
        manche.info.mises[:] = [100, 50, 50]
        print(manche.info.joueurs)
        # WHEN
        Test_Manche.remplir_board(manche)
        gains = manche.gains()
        print(gains)
        # THEN
        assert gains[manche.info.joueurs[0]] == 200
        assert gains == {1: 200}

    def test_manche_init_info_type_error(self):
        # GIVEN/WHEN/THEN
        with pytest.raises(TypeError):
            Manche(info="not_info", grosse_blind=10)

    def test_manche_init_grosse_blind_type_error(self):
        # GIVEN
        joueurs = [1, 2]
        # WHEN
        info = InfoManche(joueurs)
        # THEN
        with pytest.raises(TypeError):
            Manche(info=info, grosse_blind="10")

    def test_manche_init_grosse_blind_value_error(self):
        # GIVEN
        joueurs = [1, 2]
        # WHEN
        info = InfoManche(joueurs)
        # THEN
        with pytest.raises(ValueError):
            Manche(info=info, grosse_blind=1)

    def test_manche_nouveau_tour_exception(self, manche):
        # GIVEN/WHEN
        manche._Manche__tour = 3
        # THEN
        with pytest.raises(ValueError):
            manche.nouveau_tour()

    def test_manche_suivre_limits(self):
        # GIVEN
        joueurs = [1, 2]
        # WHEN
        info = InfoManche(joueurs)
        manche = Manche(info, 10)

        info.mises[1] = 50
        # THEN
        with pytest.raises(ValueError):
            manche.suivre(0, 20, relance=0)

    def test_classement_ex_aequo(self, manche):
        # GIVEN
        manche.board.cartes.clear()
        board = [
            Carte("As", "Coeur"),
            Carte("As", "Pique"),
            Carte("As", "Trêfle"),
            Carte("As", "Carreau"),
            Carte("2", "Coeur"),
        ]

        for carte in board:
            manche.board.ajouter_carte(carte)

        manche.tour = 3

        manche.info.assignation_mains(
            [
                Main([Carte("Roi", "Coeur"), Carte("3", "Coeur")]),
                Main([Carte("Roi", "Pique"), Carte("6", "Pique")]),
                Main([Carte("Dame", "Pique"), Carte("Dame", "Coeur")]),
            ]
        )
        # WHEN
        manche.info.modifier_statut(1, 3)
        classement = manche.classement()

        # THEN
        assert classement[1] != classement[0]

    def test_manche_init_info_type_error_1(self):
        # GIVEN/WHEN/THEN
        with pytest.raises(TypeError):
            Manche(info="not_info", grosse_blind=10)

    def test_manche_init_grosse_blind_type_error_1(self, joueurs):
        # GIVEN/WHEN
        info = InfoManche(joueurs)
        # THEN
        with pytest.raises(TypeError):
            Manche(info=info, grosse_blind="10")

    def test_manche_init_grosse_blind_value_error_1(self, joueurs):
        # GIVEN/WHEN
        info = InfoManche(joueurs)
        # THEN
        with pytest.raises(ValueError):
            Manche(info=info, grosse_blind=1)

    def test_action_exceptions(self, manche, joueurs):
        # GIVEN/WHEN/THEN
        with pytest.raises(Exception, match="Ce n'est pas à vous de jouer !"):
            manche.action(joueurs[1], "checker")

        # GIVEN/WHEN
        manche._Manche__fin = True
        # THEN
        with pytest.raises(Exception, match="La manche est déjà terminée"):
            manche.action(joueurs[0], "checker")
        manche._Manche__fin = False

        # THEN
        with pytest.raises(ValueError, match="L'action danser n'existe pas"):
            manche.action(joueurs[0], "danser")

    def test_indice_joueur_suivant_all_couches(self, manche):
        # GIVEN/WHEN
        manche.info.statuts[:] = [3, 3, 3]
        # THEN
        with pytest.raises(ValueError):
            manche.indice_joueur_suivant()

    def test_suivre_joueur_doit_all_in(self):
        # GIVEN
        joueurs = [1, 2]
        # WHEN
        info = InfoManche(joueurs)
        manche = Manche(info, 10)
        info.mises[1] = 50
        # THEN
        with pytest.raises(ValueError, match="Le joueur doit all-in"):
            manche.suivre(0, 10, relance=1)

    def test_all_in_joueur_deja_couche(self, manche):
        # GIVEN/WHEN
        manche.info.statuts[0] = 3
        # THEN
        with pytest.raises(ValueError):
            manche.all_in(0, 100)

    def test_suivre_relance_trop_grande(self):
        # GIVEN
        joueurs = [1, 2]
        # WHEN
        info = InfoManche(joueurs)
        manche = Manche(info, 10)
        info.mises[0] = 10
        info.mises[1] = 50
        # THEN
        with pytest.raises(ValueError, match="Le joueur ne peut relancer autant"):
            manche.suivre(0, 50, relance=50)

    def test_fin_de_manche_all_couches(self, manche):
        # GIVEN/WHEN
        manche.info.statuts[:] = [3, 3, 3]
        # THEN
        with pytest.raises(ValueError):
            manche.fin_de_manche()

    def test_action_checker_suivre_all_in_se_coucher(self, manche, joueurs):
        # GIVEN/WHEN
        montant = manche.action(joueurs[0], "checker")
        # THEN
        assert montant is None or isinstance(montant, int)

        # GIVEN/WHEN
        montant = manche.action(joueurs[1], "suivre", 100, relance=1)
        # THEN
        assert isinstance(montant, int)

        # GIVEN/WHEN
        montant = manche.action(joueurs[2], "all-in", 100)
        # THEN
        assert isinstance(montant, int)

        # GIVEN/WHEN
        manche.action(joueurs[0], "se coucher")
        # THEN
        assert manche.info.statuts[0] == 3
