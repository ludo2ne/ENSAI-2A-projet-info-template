"""Implémentation des tests pour toutes les sous-classes de la classe AbstractListeCartes"""

from abc import ABC

import pytest

from business_object.liste_cartes import AbstractListeCartes


class AbstractListeCartesTest(ABC):
    @pytest.fixture
    def liste_cartes(self) -> AbstractListeCartes:
        """
        Fixture à implémenter dans les sous-classes.

        IMPORTANT :
        Chaque sous-classe doit fournir une liste contenant exactement deux cartes :
        - As de pique
        - 10 de coeur
        """
        raise NotImplementedError

    @pytest.fixture
    def cls(self):
        return NotImplementedError

    def test_liste_cartes_init_succes(self, cls):
        # GIVEN
        # cls en fixture
        cartes = [pytest.trois_carreau, pytest.quatre_carreau]

        # WHEN
        liste_cartes = cls(cartes, False)

        # THEN
        assert liste_cartes.cartes == cartes

    def test_liste_cartes_init_tuple_echec(self, cls):
        # GIVEN
        # cls en fixture
        cartes = (pytest.cinq_pique, pytest.valet_coeur)
        message_attendu = f"cartes n'est pas list ou None : {type(cartes)}"

        # WHEN / THEN
        with pytest.raises(TypeError, match=message_attendu):
            cls(cartes)

    def test_liste_cartes_init_pas_carte_echec(self, cls):
        # GIVEN
        # cls en fixture
        nombre = 5
        cartes = [pytest.cinq_pique, nombre]
        message_attendu = f"cartes ne doit contenir que des objet de type Carte : {type(nombre)}"

        # WHEN / THEN
        with pytest.raises(TypeError, match=message_attendu):
            cls(cartes)

    def test_liste_cartes_str(self, liste_cartes):
        # GIVEN
        # liste_carte en fixture
        resultat = "[As de pique, 10 de coeur]"

        # WHEN
        affichage = str(liste_cartes)

        # THEN
        assert affichage == resultat

    def test_liste_cartes_len(self, liste_cartes):
        # GIVEN
        # liste_carte en fixture
        resultat = 2

        # WHEN
        longueur = len(liste_cartes)

        # THEN
        assert longueur == resultat

    def test_liste_cartes_ajouter_carte_succes(self, cls, liste_cartes):
        # GIVEN
        # liste_carte en fixture
        carte = pytest.cinq_trefle
        resultat = [pytest.as_pique, pytest.dix_coeur, pytest.cinq_trefle]

        # WHEN
        liste_cartes.ajouter_carte(carte)

        # THEN
        assert liste_cartes.cartes == resultat

    def test_liste_cartes_ajouter_carte_echec(self, liste_cartes):
        # GIVEN
        # liste_cartes en fixture
        carte = 2
        message_attendu = f"l'objet à ajouter n'est pas de type Carte : {type(carte)}"

        # WHEN / THEN
        with pytest.raises(TypeError, match=message_attendu):
            liste_cartes.ajouter_carte(carte)

    def test_liste_cartes_retirer_carte_succes(self, liste_cartes):
        # GIVEN
        # liste_cartes en fixture
        resultat = [pytest.dix_coeur]

        # WHEN
        carte_retiree = liste_cartes.retirer_carte(0)

        # THEN
        assert carte_retiree == pytest.as_pique
        assert liste_cartes.cartes == resultat

    def test_liste_cartes_retirer_carte_indice_non_int(self, liste_cartes):
        # GIVEN
        # liste_cartes en fixture
        indice = "1"
        message_attendu = f"L'indice renseigné n'est pas de type int : {type(indice)}"

        # WHEN / THEN
        with pytest.raises(TypeError, match=message_attendu):
            liste_cartes.retirer_carte(indice)

    def test_liste_cartes_retirer_carte_indice_trop_grand(self, liste_cartes):
        # GIVEN
        # liste_cartes en fixture
        indice = 2
        message_attendu = f"L'indice renseigné est trop grand : {indice}"

        # WHEN / THEN
        with pytest.raises(ValueError, match=message_attendu):
            liste_cartes.retirer_carte(indice)

    def test_liste_cartes_melanger(self, cls):
        # GIVEN
        # cls en fixture
        liste_carte = cls(None, True)
        liste_carte_temoin = cls(None, True)

        # WHEN
        liste_carte.melanger()

        # THEN
        assert liste_carte.cartes != liste_carte_temoin.cartes

    def test_liste_cartes_eq_type_diff(self, liste_cartes):
        # GIVEN
        autre = "pas une liste de cartes"

        # WHEN / THEN
        assert (liste_cartes == autre) is False


    def test_liste_cartes_eq_ordre_diff(self, cls):
        # GIVEN
        cartes1 = [pytest.as_pique, pytest.dix_coeur]
        cartes2 = [pytest.dix_coeur, pytest.as_pique]

        liste1 = cls(cartes1, False)
        liste2 = cls(cartes2, False)

        # WHEN / THEN
        assert (liste1 == liste2) is False


    def test_liste_cartes_eq_contenu_diff(self, cls):
        # GIVEN
        cartes1 = [pytest.as_pique, pytest.dix_coeur]
        cartes2 = [pytest.as_pique, pytest.cinq_trefle]

        liste1 = cls(cartes1, False)
        liste2 = cls(cartes2, False)

        # WHEN / THEN
        assert (liste1 == liste2) is False


    def test_liste_cartes_eq_succes(self, cls):
        # GIVEN
        cartes = [pytest.as_pique, pytest.dix_coeur]

        liste1 = cls(cartes, False)
        liste2 = cls(cartes, False)

        # WHEN / THEN
        assert (liste1 == liste2) is True

    def test_liste_cartes_retirer_carte_liste_vide(self, cls):
        # GIVEN
        liste = cls([], False)
        message_attendu = "La liste de cartes est vide, aucune carte ne peut être retirée."

        # WHEN / THEN
        with pytest.raises(Exception, match=message_attendu):
            liste.retirer_carte()
