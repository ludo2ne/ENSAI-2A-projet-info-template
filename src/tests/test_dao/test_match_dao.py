import os
import pytest

from unittest.mock import patch

from utils.reset_database import ResetDatabase
from utils.securite import hash_password

from dao.match_dao import MatchDao

from business_object.Match import Match


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialisation des données de test"""
    with patch.dict(os.environ, {"SCHEMA": "projet_test_dao"}):
        ResetDatabase().lancer(test_dao=True)
        yield


def test_trouver_par_id_existant():
    """Recherche par id d'un match existant"""

    # GIVEN
    match_id = 998

    # WHEN
    match = MatchDao().trouver_par_id(match_id)

    # THEN
    assert match is not None


def test_trouver_par_id_non_existant():
    """Recherche par id d'un match n'existant pas"""

    # GIVEN
    match_id = 9999999999999

    # WHEN
    match = MatchDao().trouver_par_id(match_id)

    # THEN
    assert match is None


def test_trouver_par_dates_existant():
    """Recherche par id d'un match existant"""

    # GIVEN
    dates = "2024-10-08"

    # WHEN
    match = MatchDao().trouver_par_dates(dates)

    # THEN
    assert match is not None


def test_trouver_par_dates_non_existante():
    """Recherche par une dates de match n'existant pas"""

    # GIVEN
    dates = "1024-10-08T22:00:00Z"

    # WHEN
    match = MatchDao().trouver_par_dates(dates)

    # THEN
    assert match is None


def test_trouver_match_id_par_joueur_existant():
    """Recherche par nom d'un joueur existant"""

    # GIVEN
    joueur = "Diaz"

    # WHEN
    list_match_id = MatchDao().trouver_match_id_par_joueur(joueur)

    # THEN
    assert list_match_id is not None


def test_trouver_match_id_par_joueur_non_existante():
    """Recherche par nom d'un joueur n'existant pas"""

    # GIVEN
    joueur = "Diazopoooo"

    # WHEN
    list_match_id = MatchDao().trouver_match_id_par_joueur(joueur)

    # THEN
    assert list_match_id is None


def test_trouver_match_id_par_equipe_existant():
    """Recherche par nom d'un equipe existant"""

    # GIVEN
    equipe = "give me my money"

    # WHEN
    list_match_id = MatchDao().trouver_match_id_par_equipe(equipe)

    # THEN
    assert list_match_id is not None


def test_trouver_match_id_par_equipe_non_existante():
    """Recherche par nom d'une equipe n'existant pas"""

    # GIVEN
    equipe = "fake_ team_I_guess"

    # WHEN
    list_match_id = MatchDao().trouver_match_id_par_equipe(equipe)

    # THEN
    assert list_match_id is None


def test_lister_tous():
    """Vérifie que la méthode renvoie une liste de Match
    de taille supérieure ou égale à 2
    """

    # GIVEN

    # WHEN
    matchs = MatchDao().lister_tous()

    # THEN
    assert isinstance(matchs, list)
    for j in matchs:
        assert isinstance(j, match)
    assert len(matchs) >= 2


def test_creer_ok():
    """Création de match réussie"""

    # GIVEN
    match = Match(
        match_id=13223,
        equipe1="LOS",
        equipe2="ROI",
        score1=1,
        score2=10,
        dates=2024 - 10 - 10,
        region="France",
        ligue="USBG",
        perso=False,
    )

    # WHEN
    creation_ok = MatchDao().creer(match)

    # THEN
    assert creation_ok
    assert match.match_id


def test_creer_ko():
    """Création de Match échouée (age et mail incorrects)"""

    # GIVEN
    match = Match(
        match_id=13223,
        equipe1="LOS",
        equipe2="ROI",
        score1=1,
        score2=10,
        dates=2024 - 10 - 10,
        region="France",
        ligue="USBG",
        perso=False,
    )

    # WHEN
    creation_ok = MatchDao().creer(match)

    # THEN
    assert not creation_ok


if __name__ == "__main__":
    pytest.main([__file__])
