import pytest
from business_object.Tournoi import Tournoi
from business_object.Equipe import Equipe


@pytest.fixture
def tournoi_personnel():
    return Tournoi(nom_tournoi="Tournoi Personnel", createur="Utilisateur1", officiel=False)


def tournoi_officiel():
    return Tournoi(nom_tournoi="Tournoi Officiel", createur="Utilisateur1", officiel=True)


def equipe1():
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


def equipe2():
    return Equipe(
        match_id=1,
        equipe_nom="Equipe B",
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
        equipe_score=2,
        equipe_winner=False,
        region="Europe",
        ligue="Division 1",
        stage="Quart de finale",
    )


def test_ajouter_equipes(tournoi_personnel, equipe1, equipe2):
    tournoi_personnel.ajouter_equipes([equipe1, equipe2])
    assert equipe1 in tournoi_personnel.equipes
    assert equipe2 in tournoi_personnel.equipes


def test_inscrire_equipe(tournoi_officiel, equipe1):
    tournoi_officiel.inscrire_equipe(equipe1)
    assert equipe1 in tournoi_officiel.equipes


def test_suivre_resultat(tournoi_personnel, equipe1, equipe2):
    tournoi_personnel.ajouter_equipes([equipe1, equipe2])
    gagnant = tournoi_personnel.suivre_resultats(equipe1, equipe2)
    assert gagnant == equipe1


def test_afficher_classement(tournoi_personnel, equipe1, equipe2):  # à revoir
    tournoi_personnel.ajouter_equipe([equipe1, equipe2])
    tournoi_personnel.suivre_resultats(equipe1, equipe2)
    assert classement[0][0] == "Equipe 1"
    assert classement[0][1] == 1


def test_gagnant_tournoi(tournoi_personnel, equipe1, equipe2):
    tournoi_personnel.ajouter_equipes([equipe1, equipe2])
    tournoi_personnel.suivre_resultats(equipe1, equipe2)
    gagnant = tournoi_personnel.gagnant_tournoi()
    assert gagnant == "Equipe 1"
