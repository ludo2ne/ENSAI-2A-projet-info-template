import pytest
from business_object.Pari import Pari
from business_object.Match import Match
from business_object.Equipe import Equipe


@pytest.fixture
def equipe_valide():
    """Fixture pour créer une équipe valide."""
    return Equipe(
        match_id=1,
        equipe_nom="Equipe A",
        shots=10,
        goals=3,
        saves=5,
        assists=2,
        score=1500,
        shooting_percentage=30.0,
        time_offensive_third=120.5,
        time_defensive_third=80.2,
        time_neutral_third=60.1,
        demo_inflige=4,
        demo_recu=3,
        goal_participation=0.75,
        equipe_score=3,
        equipe_winner=True,
        region="Europe",
        ligue="Division 1",
        stage="Quart de finale",
    )


@pytest.fixture
def match_valide():
    """Fixture pour créer un match valide."""
    return Match(
        id_match=1,
        equipe1="Équipe A",
        equipe2="Équipe B",
        score1=2,
        score2=1,
        date="2024-10-22",
        ligue="Ligue 1",
        region="Région X",
        perso="Personnage Y",
        cote_match=1.5,
    )


@pytest.fixture
def pari_valide(match_valide, equipe_valide):
    """Fixture pour créer un pari valide."""
    return Pari(
        id_pari=1, match=match_valide, equipe=equipe_valide, status="En cours", montant=100.0
    )


def test_pari_initialisation_valide(pari_valide):
    """Teste la création d'un pari valide."""
    assert pari_valide.id_pari == 1
    assert pari_valide.match.id_match == 1
    assert pari_valide.equipe.equipe_nom == "Équipe A"
    assert pari_valide.status == "En cours"
    assert pari_valide.montant == 100.0


@pytest.mark.parametrize(
    "id_pari, match, equipe, status, montant, expected_error",
    [
        (
            None,
            Match(
                1,
                "Équipe A",
                "Équipe B",
                2,
                1,
                "2024-10-22",
                "Ligue 1",
                "Région X",
                "Personnage Y",
                1.5,
            ),
            equipe_valide,
            "En cours",
            100.0,
            "id_pari doit être de type int",
        ),
        (1, None, equipe_valide, "En cours", 100.0, "match doit être de type Match"),
        (
            1,
            Match(
                1,
                "Équipe A",
                "Équipe B",
                2,
                1,
                "2024-10-22",
                "Ligue 1",
                "Région X",
                "Personnage Y",
                1.5,
            ),
            None,
            "En cours",
            100.0,
            "equipe doit être de type Equipe",
        ),
        (
            1,
            Match(
                1,
                "Équipe A",
                "Équipe B",
                2,
                1,
                "2024-10-22",
                "Ligue 1",
                "Région X",
                "Personnage Y",
                1.5,
            ),
            equipe_valide,
            None,
            100.0,
            "status doit être de type str",
        ),
        (
            1,
            Match(
                1,
                "Équipe A",
                "Équipe B",
                2,
                1,
                "2024-10-22",
                "Ligue 1",
                "Région X",
                "Personnage Y",
                1.5,
            ),
            equipe_valide,
            "En cours",
            None,
            "montant doit être de type float",
        ),
    ],
)
def test_pari_initialisation_invalide(id_pari, match, equipe, status, montant, expected_error):
    """Teste les erreurs d'initialisation pour différents cas de données invalides."""
    with pytest.raises(TypeError, match=expected_error):
        Pari(id_pari, match, equipe, status, montant)


def test_calculer_gains_victoire(pari_valide):
    """Teste le calcul des gains lorsque l'équipe gagne."""
    gains = pari_valide.calculer_gains()
    assert gains == 100.0 * 1.5


def test_calculer_gains_defaite(pari_valide, equipe_valide):
    """Teste le calcul des gains lorsque l'équipe perd."""
    equipe_valide.equipe_winner = False
    gains = pari_valide.calculer_gains()
    assert gains == -100.0


def test_str_pari(pari_valide):
    """Teste la méthode __str__ de Pari."""
    representation = str(pari_valide)
    assert "Vous avez parié 100.0 pour Équipe A dans le match 1" == representation
