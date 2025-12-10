"""Implémentation des tests pour la classe Paire"""

import pytest

from business_object.carte import Carte
from business_object.combinaison.paire import Paire


class Test_Paire:
    def test_paire_init_succes(self):
        # GIVEN : cartes formant une Paire
        cartes = [
            pytest.dame_coeur,
            pytest.dame_pique,
            pytest.roi_coeur,
            pytest.valet_coeur,
            pytest.dix_coeur,
        ]

        # WHEN : création de la Paire
        paire = Paire.from_cartes(cartes)

        # THEN : vérifications
        assert paire.hauteur == "Dame"
        assert paire.kicker[0] == "Roi"
        assert all(k in Carte.VALEURS() for k in paire.kicker)


    def test_paire_init_invalide(self):
        # GIVEN : cartes sans Paire
        cartes = [pytest.dame_coeur, pytest.roi_coeur, pytest.valet_coeur]

        # WHEN / THEN : création échoue
        with pytest.raises(ValueError):
            Paire.from_cartes(cartes)

    def test_paire_est_present(self):
        # GIVEN : cartes contenant une Paire
        cartes = [
            pytest.dame_coeur,
            pytest.dame_pique,
            pytest.roi_coeur,
            pytest.valet_coeur,
            pytest.dix_coeur,
        ]

        # WHEN / THEN : méthode est_present retourne True
        assert Paire.est_present(cartes)

    def test_paire_est_present_faux(self):
        # GIVEN : cartes sans Paire
        cartes = [pytest.dame_coeur, pytest.roi_coeur, pytest.valet_coeur]

        # WHEN / THEN : méthode est_present retourne False
        assert not Paire.est_present(cartes)

    def test_paire_str_repr(self):
        # GIVEN : Paire avec kicker
        paire = Paire("Dame", ("Roi", "Valet", "10"))

        # WHEN
        texte_str = str(paire)
        texte_repr = repr(paire)

        # THEN : vérifications
        assert texte_str == "Paire Dame"
        assert texte_repr == "Paire(hauteur=Dame, kicker=('Roi', 'Valet', '10'))"

    def test_paire_str_as(self):
        # GIVEN
        paire = Paire("As", ("Roi", "Dame", "Valet"))

        # WHEN
        texte = str(paire)

        # THEN
        assert texte == "Paire d'As"

