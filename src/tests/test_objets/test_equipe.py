import pytest
from business_object.Equipe import Equipe

# Dictionnaire contenant les valeurs valides pour chaque attribut
valid_values = {
    "match_id": 1,
    "equipe_nom": "Equipe A",
    "shots": 10,
    "goals": 3,
    "saves": 5,
    "assists": 2,
    "score": 1500,
    "shooting_percentage": 30.0,
    "time_offensive_third": 120.5,
    "time_defensive_third": 80.2,
    "time_neutral_third": 60.1,
    "demo_inflige": 4,
    "demo_recu": 3,
    "goal_participation": 0.75,
    "equipe_score": 3,
    "equipe_winner": True,
    "region": "Europe",
    "ligue": "Division 1",
    "stage": "Quart de finale",
}

# Dictionnaire contenant des valeurs invalides pour chaque attribut
invalid_values = {
    "match_id": "1",  # str au lieu de int
    "equipe_nom": 123,  # int au lieu de str
    "shots": "10",  # str au lieu de int
    "goals": 3.0,  # float au lieu de int
    "saves": "5",  # str au lieu de int
    "assists": None,  # NoneType au lieu de int
    "score": "1500",  # str au lieu de int
    "shooting_percentage": "30.0",  # str au lieu de float
    "time_offensive_third": "120.5",  # str au lieu de float
    "time_defensive_third": None,  # NoneType au lieu de float
    "time_neutral_third": "60.1",  # str au lieu de float
    "demo_inflige": 4.5,  # float au lieu de int
    "demo_recu": "3",  # str au lieu de int
    "goal_participation": "0.75",  # str au lieu de float
    "equipe_score": "3",  # str au lieu de int
    "equipe_winner": "True",  # str au lieu de bool
    "region": 123,  # int au lieu de str
    "ligue": None,  # NoneType au lieu de str
    "stage": 5.0,  # float au lieu de str
}


@pytest.mark.parametrize("attr_name, invalid_value", invalid_values.items())
def test_initialisation_type_invalide(attr_name, invalid_value):
    """Test que l'initialisation avec des valeurs invalides lève une AssertionError"""
    args = valid_values.copy()
    args[attr_name] = invalid_value

    with pytest.raises(AssertionError):
        Equipe(**args)


def test_initialisation_valide():
    """Test l'initialisation de la classe Equipe avec des valeurs valides"""
    equipe = Equipe(**valid_values)
    assert equipe.match_id == 1
    assert equipe.equipe_nom == "Equipe A"
    assert equipe.shots == 10
    assert equipe.goals == 3
    assert equipe.saves == 5
    assert equipe.assists == 2
    assert equipe.score == 1500
    assert equipe.shooting_percentage == 30.0
    assert equipe.time_offensive_third == 120.5
    assert equipe.time_defensive_third == 80.2
    assert equipe.time_neutral_third == 60.1
    assert equipe.demo_inflige == 4
    assert equipe.demo_recu == 3
    assert equipe.goal_participation == 0.75
    assert equipe.equipe_score == 3
    assert equipe.equipe_winner is True
    assert equipe.region == "Europe"
    assert equipe.ligue == "Division 1"
    assert equipe.stage == "Quart de finale"


def test_str_representation():
    """Test de la méthode __str__ de la classe Equipe"""
    equipe = Equipe(**valid_values)
    expected_str = "Equipe(Equipe A, Score: 3, Région: Europe, Vainqueur: Oui)"
    assert str(equipe) == expected_str
