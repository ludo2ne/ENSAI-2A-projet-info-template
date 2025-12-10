import pytest

from business_object.combinaison.double_paire import DoublePaire


class Test_DoublePaireCartes:
    def test_double_paire_init_succes(self):
        # GIVEN :
        cartes = [
            pytest.roi_coeur,
            pytest.roi_carreau,
            pytest.dame_coeur,
            pytest.dame_pique,
            pytest.valet_coeur,
            pytest.neuf_trefle,
            pytest.huit_carreau,
        ]

        # WHEN : création de la Double Paire
        double_paire = DoublePaire.from_cartes(cartes)

        # THEN : vérification des deux paires et du kicker
        assert double_paire.hauteur == ["Roi", "Dame"]
        assert double_paire.kicker == "Valet"
        assert DoublePaire.FORCE() == 2

    def test_double_paire_init_invalide(self):
        # GIVEN :
        cartes = [
            pytest.roi_coeur,
            pytest.dame_coeur,
            pytest.valet_coeur,
            pytest.neuf_coeur,
            pytest.huit_coeur,
            pytest.sept_coeur,
            pytest.six_coeur,
        ]

        # WHEN / THEN : doit lever ValueError
        with pytest.raises(ValueError, match="Aucune Double Paire présente"):
            DoublePaire.from_cartes(cartes)

    def test_double_paire_est_present(self):
        # GIVEN : main avec Double Paire
        cartes = [
            pytest.roi_coeur,
            pytest.roi_carreau,
            pytest.dame_coeur,
            pytest.dame_pique,
            pytest.valet_coeur,
            pytest.neuf_trefle,
            pytest.huit_carreau,
        ]

        # THEN : est_present retourne True
        assert DoublePaire.est_present(cartes)

    def test_double_paire_est_present_faux(self):
        # GIVEN : main sans Double Paire
        cartes = [
            pytest.roi_coeur,
            pytest.dame_coeur,
            pytest.valet_coeur,
            pytest.neuf_coeur,
            pytest.huit_coeur,
            pytest.sept_coeur,
            pytest.six_coeur,
        ]

        # THEN : est_present retourne False
        assert not DoublePaire.est_present(cartes)

    def test_double_paire_comparaison(self):
        # GIVEN : deux mains avec Double Paire différente
        cartes_1 = [
            pytest.roi_coeur,
            pytest.roi_carreau,
            pytest.dame_coeur,
            pytest.dame_pique,
            pytest.valet_coeur,
            pytest.neuf_trefle,
            pytest.huit_carreau,
        ]
        cartes_2 = [
            pytest.dame_coeur,
            pytest.dame_pique,
            pytest.valet_coeur,
            pytest.valet_pique,
            pytest.as_coeur,
            pytest.neuf_coeur,
            pytest.huit_coeur,
        ]

        dp1 = DoublePaire.from_cartes(cartes_1)
        dp2 = DoublePaire.from_cartes(cartes_2)

        # THEN : comparaison correcte
        assert dp1 > dp2
        assert dp2 < dp1
        assert dp1 == DoublePaire.from_cartes(cartes_1)

    def test_double_paire_str_repr(self):
        # GIVEN :
        cartes = [
            pytest.roi_coeur,
            pytest.roi_carreau,
            pytest.dame_coeur,
            pytest.dame_pique,
            pytest.valet_coeur,
            pytest.neuf_trefle,
            pytest.huit_carreau,
        ]

        # WHEN : création
        double_paire = DoublePaire.from_cartes(cartes)

        # THEN : représentation lisible
        assert str(double_paire) == "Double Paire Roi Dame"
        assert repr(double_paire) == f"DoublePaire(hauteur={['Roi', 'Dame']}, kicker=Valet)"
