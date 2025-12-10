"""Fichier de configuration pour les tests"""

import pytest

from business_object.carte import Carte


def pytest_configure():
    # Pique
    pytest.deux_pique = Carte("2", "Pique")
    pytest.trois_pique = Carte("3", "Pique")
    pytest.quatre_pique = Carte("4", "Pique")
    pytest.cinq_pique = Carte("5", "Pique")
    pytest.six_pique = Carte("6", "Pique")
    pytest.sept_pique = Carte("7", "Pique")
    pytest.huit_pique = Carte("8", "Pique")
    pytest.neuf_pique = Carte("9", "Pique")
    pytest.dix_pique = Carte("10", "Pique")
    pytest.valet_pique = Carte("Valet", "Pique")
    pytest.dame_pique = Carte("Dame", "Pique")
    pytest.roi_pique = Carte("Roi", "Pique")
    pytest.as_pique = Carte("As", "Pique")

    # Carreau
    pytest.deux_carreau = Carte("2", "Carreau")
    pytest.trois_carreau = Carte("3", "Carreau")
    pytest.quatre_carreau = Carte("4", "Carreau")
    pytest.cinq_carreau = Carte("5", "Carreau")
    pytest.six_carreau = Carte("6", "Carreau")
    pytest.sept_carreau = Carte("7", "Carreau")
    pytest.huit_carreau = Carte("8", "Carreau")
    pytest.neuf_carreau = Carte("9", "Carreau")
    pytest.dix_carreau = Carte("10", "Carreau")
    pytest.valet_carreau = Carte("Valet", "Carreau")
    pytest.dame_carreau = Carte("Dame", "Carreau")
    pytest.roi_carreau = Carte("Roi", "Carreau")
    pytest.as_carreau = Carte("As", "Carreau")

    # Coeur
    pytest.deux_coeur = Carte("2", "Coeur")
    pytest.trois_coeur = Carte("3", "Coeur")
    pytest.quatre_coeur = Carte("4", "Coeur")
    pytest.cinq_coeur = Carte("5", "Coeur")
    pytest.six_coeur = Carte("6", "Coeur")
    pytest.sept_coeur = Carte("7", "Coeur")
    pytest.huit_coeur = Carte("8", "Coeur")
    pytest.neuf_coeur = Carte("9", "Coeur")
    pytest.dix_coeur = Carte("10", "Coeur")
    pytest.valet_coeur = Carte("Valet", "Coeur")
    pytest.dame_coeur = Carte("Dame", "Coeur")
    pytest.roi_coeur = Carte("Roi", "Coeur")
    pytest.as_coeur = Carte("As", "Coeur")

    # Trêfle
    pytest.deux_trefle = Carte("2", "Trêfle")
    pytest.trois_trefle = Carte("3", "Trêfle")
    pytest.quatre_trefle = Carte("4", "Trêfle")
    pytest.cinq_trefle = Carte("5", "Trêfle")
    pytest.six_trefle = Carte("6", "Trêfle")
    pytest.sept_trefle = Carte("7", "Trêfle")
    pytest.huit_trefle = Carte("8", "Trêfle")
    pytest.neuf_trefle = Carte("9", "Trêfle")
    pytest.dix_trefle = Carte("10", "Trêfle")
    pytest.valet_trefle = Carte("Valet", "Trêfle")
    pytest.dame_trefle = Carte("Dame", "Trêfle")
    pytest.roi_trefle = Carte("Roi", "Trêfle")
    pytest.as_trefle = Carte("As", "Trêfle")
