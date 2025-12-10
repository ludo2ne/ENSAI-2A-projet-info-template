import pytest

from business_object.combinaison.simple import Simple


class Test_Simple:
    def test_simple_creation_simple(self):
        # GIVEN :
        cartes = [
            pytest.as_coeur,
            pytest.roi_carreau,
            pytest.dame_coeur,
            pytest.valet_pique,
            pytest.dix_carreau,
            pytest.neuf_coeur,
            pytest.huit_pique,
        ]

        # WHEN : création de la Simple
        simple = Simple.from_cartes(cartes)

        # THEN : vérifications
        assert simple.hauteur == "As"  # la carte la plus haute
        assert simple.kicker == ("Roi", "Dame", "Valet", "10")  # les 4 suivants
        assert Simple.FORCE() == 0

    def test_simple_est_present(self):
        # GIVEN : des cartes non vides
        cartes = [
            pytest.as_coeur,
            pytest.roi_carreau,
            pytest.dame_coeur,
            pytest.valet_pique,
            pytest.dix_carreau,
        ]

        # WHEN / THEN
        assert Simple.est_present(cartes)

    def test_simple_est_present_faux(self):
        # GIVEN : aucune carte
        cartes = []

        # WHEN / THEN
        assert not Simple.est_present(cartes)

    def test_simple_str_repr(self):
        # GIVEN : création d'une Simple
        cartes = [
            pytest.as_coeur,
            pytest.roi_carreau,
            pytest.dame_coeur,
            pytest.valet_pique,
            pytest.dix_carreau,
            pytest.neuf_coeur,
            pytest.huit_pique,
        ]
        simple = Simple.from_cartes(cartes)

        # WHEN
        texte_str = str(simple)
        texte_repr = repr(simple)

        # THEN : vérifications
        assert texte_str == "Simple As"
        assert texte_repr == "Simple(hauteur='As', kicker=('Roi', 'Dame', 'Valet', '10'))"
