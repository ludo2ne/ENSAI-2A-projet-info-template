import pytest
from business_object.joueur import Joueur

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
    "nom": "John Doe",
    "nationalite": "Française",
    "region": "Europe",
    "rating": 8.5,
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
    "nom": 123,  # int au lieu de str
    "nationalite": 456,  # int au lieu de str
    "region": None,  # NoneType au lieu de str
    "rating": "8.5",  # str au lieu de float
}


@pytest.mark.parametrize("attr_name, invalid_value", invalid_values.items())
def test_initialisation_type_invalide(attr_name, invalid_value):
    args = valid_values.copy()
    args[attr_name] = invalid_value

    with pytest.raises(AssertionError):
        Joueur(**args)


def test_initialisation_valide():
    """Test l'initialisation de la classe"""
    joueur = Joueur(**valid_values)
    assert joueur.match_id == 1
    assert joueur.equipe_nom == "Equipe A"
    assert joueur.shots == 10
    assert joueur.goals == 3
    assert joueur.saves == 5
    assert joueur.assists == 2
    assert joueur.score == 1500
    assert joueur.shooting_percentage == 30.0
    assert joueur.time_offensive_third == 120.5
    assert joueur.time_defensive_third == 80.2
    assert joueur.time_neutral_third == 60.1
    assert joueur.demo_inflige == 4
    assert joueur.demo_recu == 3
    assert joueur.goal_participation == 0.75
    assert joueur.nom == "John Doe"
    assert joueur.nationalite == "Française"
    assert joueur.region == "Europe"
    assert joueur.rating == 8.5


def test_str_representation():
    """Test de la méthode __str__"""
    joueur = Joueur(**valid_values)
    expected_str = "Joueur(John Doe, Nationalité: Française, Région: Europe, Rating: 8.5)"
    assert str(joueur) == expected_str
