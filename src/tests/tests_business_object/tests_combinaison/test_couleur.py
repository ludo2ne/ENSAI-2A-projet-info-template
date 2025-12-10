import pytest

from business_object.combinaison.couleur import Couleur


class Test_Couleur:
    def test_couleur_init_succes(self):
        # GIVEN :
        cartes = [
            pytest.as_coeur,
            pytest.roi_coeur,
            pytest.dame_coeur,
            pytest.valet_coeur,
            pytest.neuf_coeur,
            pytest.deux_carreau,
            pytest.trois_pique,
        ]

        # WHEN : création de la Couleur
        couleur = Couleur.from_cartes(cartes)

        # THEN : vérifier que la meilleure couleur est choisie
        assert couleur.hauteur == ["As", "Roi", "Dame", "Valet", "9"]
        assert couleur.kicker is None
        assert Couleur.FORCE() == 5

    def test_couleur_init_erreur(self):
        # GIVEN : moins de 5 cartes de même couleur
        cartes = [
            pytest.as_coeur,
            pytest.roi_coeur,
            pytest.dame_coeur,
            pytest.valet_coeur,
            pytest.neuf_pique,
            pytest.deux_carreau,
            pytest.trois_trefle,
        ]

        # WHEN / THEN : doit lever ValueError
        with pytest.raises(ValueError, match="Aucune Couleur présente"):
            Couleur.from_cartes(cartes)

    def test_couleur_comparaison(self):
        # GIVEN : deux mains avec Couleur différente
        cartes_as = [
            pytest.as_coeur,
            pytest.roi_coeur,
            pytest.dame_coeur,
            pytest.valet_coeur,
            pytest.neuf_coeur,
            pytest.deux_carreau,
            pytest.trois_pique,
        ]
        cartes_roi = [
            pytest.roi_pique,
            pytest.dame_pique,
            pytest.valet_pique,
            pytest.dix_pique,
            pytest.neuf_pique,
            pytest.as_coeur,
            pytest.deux_coeur,
        ]

        couleur_as = Couleur.from_cartes(cartes_as)
        couleur_roi = Couleur.from_cartes(cartes_roi)

        # THEN : comparaison correcte carte par carte
        assert couleur_as > couleur_roi
        assert couleur_roi < couleur_as
        assert couleur_as == Couleur.from_cartes(cartes_as)

    def test_couleur_str_repr(self):
        # GIVEN :
        cartes = [
            pytest.as_coeur,
            pytest.roi_coeur,
            pytest.dame_coeur,
            pytest.valet_coeur,
            pytest.neuf_coeur,
            pytest.deux_carreau,
            pytest.trois_pique,
        ]
        couleur = Couleur.from_cartes(cartes)

        # THEN : chaînes correctes
        assert str(couleur) == "Couleur"
        assert repr(couleur) == f"Couleur(hauteur={['As', 'Roi', 'Dame', 'Valet', '9']})"

    def test_couleur_est_present(self):
        # GIVEN : main avec Couleur
        cartes = [
            pytest.as_coeur,
            pytest.roi_coeur,
            pytest.dame_coeur,
            pytest.valet_coeur,
            pytest.neuf_coeur,
            pytest.deux_carreau,
            pytest.trois_pique,
        ]
        # THEN
        assert Couleur.est_present(cartes)

    def test_couleur_est_present_faux(self):
        # GIVEN :
        cartes = [
            pytest.as_coeur,
            pytest.roi_coeur,
            pytest.dame_coeur,
            pytest.valet_coeur,
            pytest.neuf_pique,
            pytest.deux_carreau,
            pytest.trois_trefle,
        ]
        # THEN
        assert not Couleur.est_present(cartes)
