import pytest

from business_object.combinaison.carre import Carre


class Test_Carre:
    def test_carre_init_succes(self):
        # GIVEN
        cartes = [
            pytest.roi_coeur,
            pytest.roi_trefle,
            pytest.roi_carreau,
            pytest.roi_pique,
            pytest.as_coeur,
            pytest.dame_trefle,
            pytest.neuf_carreau,
        ]

        # WHEN : création du Carré
        carre = Carre.from_cartes(cartes)

        # THEN : vérifier hauteur et kicker
        assert carre.hauteur == "Roi"
        assert carre.kicker == "As"
        assert Carre.FORCE() == 7

    def test_carre_init_erreur(self):
        # GIVEN : cartes sans Carré
        cartes = [
            pytest.dame_coeur,
            pytest.dame_trefle,
            pytest.dame_carreau,  # juste un brelan
            pytest.as_pique,
            pytest.roi_coeur,
            pytest.neuf_carreau,
            pytest.deux_trefle,
        ]

        # WHEN / THEN : création échoue
        with pytest.raises(ValueError, match="Aucun Carré présent"):
            Carre.from_cartes(cartes)

    def test_carre_comparaison(self):
        # GIVEN : deux Carrés différents
        carre_roi = Carre.from_cartes(
            [
                pytest.roi_coeur,
                pytest.roi_trefle,
                pytest.roi_carreau,
                pytest.roi_pique,
                pytest.as_coeur,
                pytest.dame_trefle,
                pytest.neuf_carreau,
            ]
        )
        carre_dame = Carre.from_cartes(
            [
                pytest.dame_coeur,
                pytest.dame_trefle,
                pytest.dame_carreau,
                pytest.dame_pique,
                pytest.as_coeur,
                pytest.roi_trefle,
                pytest.neuf_carreau,
            ]
        )

        # THEN : comparaison fonctionne
        assert carre_roi > carre_dame
        assert not carre_dame > carre_roi
        assert carre_dame == Carre.from_cartes(
            [
                pytest.dame_coeur,
                pytest.dame_trefle,
                pytest.dame_carreau,
                pytest.dame_pique,
                pytest.as_coeur,
                pytest.roi_trefle,
                pytest.neuf_carreau,
            ]
        )

    def test_carre_str_repr(self):
        # GIVEN : Carré de Roi
        cartes = [
            pytest.roi_coeur,
            pytest.roi_trefle,
            pytest.roi_carreau,
            pytest.roi_pique,
            pytest.as_coeur,
            pytest.dame_trefle,
            pytest.neuf_carreau,
        ]
        carre = Carre.from_cartes(cartes)

        # THEN : __str__ et __repr__
        assert str(carre) == "Carre de Roi"
        assert repr(carre) == f"Carre(hauteur={carre.hauteur}, kicker={carre.kicker})"

    def test_carre_str_as(self):
        # GIVEN : Carré d'As
        cartes = [
            pytest.as_coeur,
            pytest.as_trefle,
            pytest.as_carreau,
            pytest.as_pique,
            pytest.roi_coeur,
            pytest.dame_trefle,
            pytest.neuf_carreau,
        ]
        carre = Carre.from_cartes(cartes)

        # THEN : représentation spéciale pour As
        assert str(carre) == "Carre d'As"

    def test_carre_est_present(self):
        # GIVEN : cartes avec et sans Carré
        cartes_ok = [
            pytest.roi_coeur,
            pytest.roi_trefle,
            pytest.roi_carreau,
            pytest.roi_pique,
            pytest.as_coeur,
            pytest.dame_trefle,
            pytest.neuf_carreau,
        ]
        cartes_non = [
            pytest.dame_coeur,
            pytest.dame_trefle,
            pytest.dame_carreau,
            pytest.as_pique,
            pytest.roi_coeur,
            pytest.neuf_carreau,
            pytest.deux_trefle,
        ]

        # THEN : est_present correct
        assert Carre.est_present(cartes_ok)
        assert not Carre.est_present(cartes_non)
