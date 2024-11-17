import pytest
from business_object.Utilisateur import Utilisateur
from business_object.Tournoi import Tournoi
from business_object.Pari import Pari
from business_object.Match import Match
from business_object.Equipe import Equipe


@pytest.fixture
def tournoi_exemple():
    """Fixture pour créer un exemple de tournoi."""
    return Tournoi(id_tournoi="1", nom_tournoi="Championnat", equipes=[])


@pytest.fixture
def pari_exemple():
    """Fixture pour créer un exemple de pari."""
    match = Match(id_match=1, cote_match=1.5)
    equipe = Equipe(equipe_nom="Team A", equipe_winner=True)
    return Pari(id_pari=1, match=match, equipe=equipe, status="En cours", montant=50.0)


@pytest.fixture
def utilisateur_avec_donnees(tournoi_exemple, pari_exemple):
    """Fixture pour créer un utilisateur avec des tournois et paris."""
    tournois = [tournoi_exemple]
    paris = [pari_exemple]
    return Utilisateur(
        nom_utilisateur="TestUser",
        mot_de_passe="password123",
        email="testuser@example.com",
        tournois_crees=tournois,
        paris=paris,
        points=100,
    )


def test_utilisateur_initialisation(utilisateur_avec_donnees, tournoi_exemple, pari_exemple):
    """Teste la création d'un Utilisateur valide avec des tournois et des paris."""
    assert utilisateur_avec_donnees.nom_utilisateur == "TestUser"
    assert utilisateur_avec_donnees.mot_de_passe == "password123"
    assert utilisateur_avec_donnees.email == "testuser@example.com"
    assert utilisateur_avec_donnees.points == 100

    # Vérification du contenu des listes
    assert utilisateur_avec_donnees.tournois_crees == [tournoi_exemple]
    assert utilisateur_avec_donnees.paris == [pari_exemple]


def test_str_utilisateur(utilisateur_avec_donnees):
    """Teste la méthode __str__ d'Utilisateur."""
    expected_str = (
        "identifiant:TestUser, mdp:password123, email:testuser@example.com"
        "tournois:[<Tournoi object>], paris:[<Pari object>], points:100"
    )
    assert str(utilisateur_avec_donnees) == expected_str
