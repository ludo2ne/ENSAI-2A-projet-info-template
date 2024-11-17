import os
import pytest
from datetime import datetime
from unittest.mock import patch
from business_object.Match import Match
from service.calendrier_evenement import CalendrierEvenement


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialisation des données de test"""
    with patch.dict(os.environ, {"SCHEMA": "projet_test_dao"}):
        ResetDatabase().lancer(test_dao=True)
        yield


def test_rechercher_match_par_date():
    #GIVEN
    date = "2024-10-08T22:00:00Z"

    #WHEN
    match = CalendrierEvenement.rechercher_match_par_date(date)

    #THEN
    assert isinstance(match, Match)


# Exécution du test
test_rechercher_match_par_date()


if __name__ == "__main__":
    pytest.main([__file__])
