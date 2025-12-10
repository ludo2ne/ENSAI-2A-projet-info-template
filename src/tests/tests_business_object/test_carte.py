"""Implémentation des tests pour la classe Carte"""

import pytest

from business_object.carte import Carte


class TestCarte:
    def test_carte_init_succes(self):
        # GIVEN
        valeur = "Roi"
        couleur = "Pique"

        # WHEN
        carte = Carte(valeur, couleur)

        # THEN
        assert carte == pytest.roi_pique

    def test_carte_init_valeur_incorrecte(self):
        # GIVEN
        valeur = "1"
        couleur = "Pique"
        message_attendu = f"Valeur de la carte incorrecte : {valeur}"

        # WHEN / THEN
        with pytest.raises(ValueError, match=message_attendu):
            Carte(valeur, couleur)

    def test_carte_init_couleur_incorrecte(self):
        # GIVEN
        valeur = "2"
        couleur = "noir"
        message_attendu = f"Couleur de la carte incorrecte : {couleur}"

        # WHEN / THEN
        with pytest.raises(ValueError, match=message_attendu):
            Carte(valeur, couleur)

    def test_carte_str(self):
        # GIVEN
        carte = pytest.dix_coeur
        resultat = "10 de coeur"

        # WHEN
        affichage = str(carte)

        # THEN
        assert affichage == resultat

    def test_carte_repr(self):
        # GIVEN
        carte = pytest.as_coeur
        resultat = "Carte(As, Coeur)"

        # WHEN
        affichage = repr(carte)

        # THEN
        assert affichage == resultat

    @pytest.mark.parametrize(
        "carte, other, resultat_attendu",
        [
            (pytest.huit_carreau, pytest.huit_carreau, True),
            (pytest.dame_carreau, pytest.valet_carreau, False),
            (pytest.quatre_pique, pytest.as_trefle, False),
            (pytest.six_pique, pytest.six_coeur, False),
            (pytest.cinq_coeur, 5, False),
            (pytest.neuf_trefle, "Trêfle", False),
        ],
    )
    def test_carte_eq_et_hash(self, carte, other, resultat_attendu):
        # GIVEN
        # paramètres injectés par parametrize

        # WHEN / THEN
        assert (carte == other) is resultat_attendu
        assert (hash(carte) == hash(other)) is resultat_attendu

    @pytest.mark.parametrize(
        "carte, other, resultat_attendu",
        [
            (pytest.deux_carreau, pytest.as_carreau, True),
            (pytest.dame_carreau, pytest.valet_carreau, False),
            (pytest.quatre_trefle, pytest.quatre_coeur, False),
        ],
    )
    def test_carte_lt_succes(self, carte, other, resultat_attendu):
        # GIVEN
        # paramètres injectés par parametrize

        # WHEN / THEN
        assert (carte < other) is resultat_attendu

    def test_carte_lt_echec(self):
        # GIVEN
        carte = pytest.dix_carreau
        other = 5
        message_attendu = f"L'objet comparé n'est pas de type Carte : {type(other)}"

        # WHEN / THEN
        with pytest.raises(TypeError, match=message_attendu):
            carte < other

    @pytest.mark.parametrize(
        "carte, other, resultat_attendu",
        [
            (pytest.roi_carreau, pytest.valet_carreau, True),
            (pytest.deux_carreau, pytest.dix_carreau, False),
            (pytest.sept_trefle, pytest.sept_coeur, False),
        ],
    )
    def test_carte_gt_succes(self, carte, other, resultat_attendu):
        # GIVEN
        # paramètres injectés par parametrize

        # WHEN / THEN
        assert (carte > other) is resultat_attendu

    def test_carte_gt_echec(self):
        # GIVEN
        carte = pytest.dix_carreau
        other = 5
        message_attendu = f"L'objet comparé n'est pas de type Carte : {type(other)}"

        # WHEN / THEN
        with pytest.raises(TypeError, match=message_attendu):
            carte > other

    @pytest.mark.parametrize(
        "carte, other, resultat_attendu",
        [
            (pytest.valet_trefle, pytest.valet_carreau, True),
            (pytest.deux_pique, pytest.dix_pique, False),
            (pytest.sept_trefle, pytest.dame_coeur, False),
        ],
    )
    def test_carte_valeur_egale_succes(self, carte, other, resultat_attendu):
        # GIVEN
        # paramètres injectés par parametrize

        # WHEN / THEN
        assert (carte.valeur_egale(other)) is resultat_attendu

    def test_carte_valeur_egale_echec(self):
        # GIVEN
        carte = pytest.quatre_carreau
        other = 4
        message_attendu = f"L'objet comparé n'est pas de type Carte : {type(other)}"

        # WHEN / THEN
        with pytest.raises(TypeError, match=message_attendu):
            carte.valeur_egale(other)
