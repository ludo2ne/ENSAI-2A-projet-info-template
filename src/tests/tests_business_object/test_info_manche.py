import pytest

from business_object.info_manche import InfoManche
from business_object.main import Main
from business_object.joueur import Joueur


class TestInfoManche:
    @pytest.fixture
    def joueurs(self):
        return [1, 2]

    @pytest.fixture
    def mains(self):
        return [
            Main([pytest.as_pique, pytest.roi_coeur]),
            Main([pytest.dix_carreau, pytest.dix_trefle]),
        ]

    # -------- Tests d'initialisation -------- #

    def test_infomanche_init_succes(self, joueurs):
        # GIVEN / WHEN
        manche = InfoManche(joueurs)

        # THEN
        assert manche.joueurs == joueurs
        assert manche.statuts == [0, 0]
        assert manche.mises == [0, 0]
        assert manche.tour_couche == [None, None]
        assert manche.mains == [None, None]

    def test_infomanche_init_TypeError_mauvais_type_liste(self):
        # GIVEN
        mauvais_param = "pas une liste"

        # WHEN / THEN
        with pytest.raises(TypeError, match="Le paramètre 'joueurs' doit être une liste"):
            InfoManche(mauvais_param)

    def test_infomanche_init_TypeError_mauvais_type_joueur(self):
        # GIVEN
        mauvais_joueurs = ["Alice", "Bob"]

        # WHEN / THEN
        with pytest.raises(TypeError, match="Tous les éléments de 'joueurs' doivent être des int"):
            InfoManche(mauvais_joueurs)

    def test_infomanche_init_ValueError_pas_assez_de_joueurs(self):
        # GIVEN / WHEN / THEN
        with pytest.raises(ValueError, match="Au moins deux joueurs doivent être présents"):
            InfoManche([])

    def test_assignation_mains_succes(self, joueurs, mains):
        # GIVEN
        manche = InfoManche(joueurs)

        # WHEN
        manche.assignation_mains(mains)

        # THEN
        assert manche.mains == mains

    def test_assignation_mains_TypeError(self, joueurs):
        # GIVEN
        manche = InfoManche(joueurs)
        mauvaises_mains = ["pas une main"]

        # WHEN / THEN
        with pytest.raises(TypeError, match="Le paramètre 'mains' doit être une liste de Main"):
            manche.assignation_mains(mauvaises_mains)

    def test_assignation_mains_ValueError_nombre_incorrect(self, joueurs, mains):
        # GIVEN
        manche = InfoManche(joueurs)
        mauvaises_mains = [mains[0]]  # 1 seule main

        # WHEN / THEN
        with pytest.raises(
            ValueError, match="Le nombre de mains doit correspondre au nombre de joueurs"
        ):
            manche.assignation_mains(mauvaises_mains)

    def test_modifier_statut(self, joueurs):
        # GIVEN
        manche = InfoManche(joueurs)

        # WHEN
        manche.modifier_statut(1, 3)

        # THEN
        assert manche.statuts[1] == 3

    def test_modifier_mise(self, joueurs):
        # GIVEN
        manche = InfoManche(joueurs)

        # WHEN
        manche.modifier_mise(0, 150)

        # THEN
        assert manche.mises[0] == 150

    def test_modifier_tour_couche(self, joueurs):
        # GIVEN
        manche = InfoManche(joueurs)

        # WHEN
        manche.modifier_tour_couche(1, 2)

        # THEN
        assert manche.tour_couche[1] == 2

    def test_str_contenu(self, joueurs):
        # GIVEN
        manche = InfoManche(joueurs)

        # WHEN
        affichage = str(manche)

        # THEN
        assert "InfoManche(" in affichage
        assert "joueurs=" in affichage
        assert "statuts=" in affichage
        assert "mains=" in affichage
        assert "mises=" in affichage
        assert "tour_couche=" in affichage

    