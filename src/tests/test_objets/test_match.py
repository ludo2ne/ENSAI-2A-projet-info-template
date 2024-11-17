import pytest
from business_object.Match import Match


def test_match_initialisation_valide():
    """Teste la création d'un objet Match avec des données valides."""
    match = Match(
        id_match=1,
        equipe1="Équipe A",
        equipe2="Équipe B",
        score1=3,
        score2=2,
        date="2024-10-22",
        ligue="Ligue 1",
        region="Région X",
        perso="Personnage Y",
        cote_match=1.5,
    )
    assert match.id_match == 1
    assert match.equipe1 == "Équipe A"
    assert match.equipe2 == "Équipe B"
    assert match.score1 == 3
    assert match.score2 == 2
    assert match.date == "2024-10-22"
    assert match.ligue == "Ligue 1"
    assert match.region == "Région X"
    assert match.perso == "Personnage Y"
    assert match.cote_match == 1.5


@pytest.mark.parametrize(
    "id_match, equipe1, equipe2, score1, score2, date, ligue, region, perso, cote_match, expected_error",
    [
        (
            None,
            "Équipe A",
            "Équipe B",
            3,
            2,
            "2024-10-22",
            "Ligue 1",
            "Région X",
            "Personnage Y",
            1.5,
            "id_match doit être un entier",
        ),
        (
            1,
            "",
            "Équipe B",
            3,
            2,
            "2024-10-22",
            "Ligue 1",
            "Région X",
            "Personnage Y",
            1.5,
            "equipe1 doit être une chaîne non vide",
        ),
        (
            1,
            "Équipe A",
            "",
            3,
            2,
            "2024-10-22",
            "Ligue 1",
            "Région X",
            "Personnage Y",
            1.5,
            "equipe2 doit être une chaîne non vide",
        ),
        (
            1,
            "Équipe A",
            "Équipe B",
            -1,
            2,
            "2024-10-22",
            "Ligue 1",
            "Région X",
            "Personnage Y",
            1.5,
            "score1 doit être un entier positif",
        ),
        (
            1,
            "Équipe A",
            "Équipe B",
            3,
            -2,
            "2024-10-22",
            "Ligue 1",
            "Région X",
            "Personnage Y",
            1.5,
            "score2 doit être un entier positif",
        ),
        (
            1,
            "Équipe A",
            "Équipe B",
            3,
            2,
            "",
            "Ligue 1",
            "Région X",
            "Personnage Y",
            1.5,
            "date doit être une chaîne non vide",
        ),
        (
            1,
            "Équipe A",
            "Équipe B",
            3,
            2,
            "2024-10-22",
            "",
            "Région X",
            "Personnage Y",
            1.5,
            "ligue doit être une chaîne non vide",
        ),
        (
            1,
            "Équipe A",
            "Équipe B",
            3,
            2,
            "2024-10-22",
            "Ligue 1",
            "",
            "Personnage Y",
            1.5,
            "region doit être une chaîne non vide",
        ),
        (
            1,
            "Équipe A",
            "Équipe B",
            3,
            2,
            "2024-10-22",
            "Ligue 1",
            "Région X",
            "",
            1.5,
            "perso doit être une chaîne non vide",
        ),
        (
            1,
            "Équipe A",
            "Équipe B",
            3,
            2,
            "2024-10-22",
            "Ligue 1",
            "Région X",
            "Personnage Y",
            0,
            "cote_match doit être un nombre positif",
        ),
    ],
)
def test_match_initialisation_invalide(
    id_match,
    equipe1,
    equipe2,
    score1,
    score2,
    date,
    ligue,
    region,
    perso,
    cote_match,
    expected_error,
):
    """Teste les erreurs d'initialisation pour différents cas de données invalides."""
    with pytest.raises(AssertionError, match=expected_error):
        Match(id_match, equipe1, equipe2, score1, score2, date, ligue, region, perso, cote_match)
