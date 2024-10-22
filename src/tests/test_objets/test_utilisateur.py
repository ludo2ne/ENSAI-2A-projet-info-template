import pytest
from business_object import Utilisateur, Tournoi, Pari


def test_utilisateur_creation():
    """Test la création d'un utilisateur"""
    nom_utilisateur = "TestUser"
    mot_de_passe = "password123"
    email = "testuser@example.com"
    tournois_crees = [Tournoi("Tournoi 1"), Tournoi("Tournoi 2")]
    paris = [Pari("Paris 1"), Pari("Paris 2")]
    points = 100

    utilisateur = Utilisateur(nom_utilisateur, mot_de_passe, email, tournois_crees, paris, points)

    assert utilisateur.nom_utilisateur == nom_utilisateur
    assert utilisateur.mot_de_passe == mot_de_passe
    assert utilisateur.email == email
    assert utilisateur.tournois_crees == tournois_crees
    assert utilisateur.paris == paris
    assert utilisateur.points == points


def test_utilisateur_str():
    """Test de l'affichage de la méthode __str__() de utilisateur"""
    utilisateur = Utilisateur(
        "PaulinleMalin", "strongmdp1234", "PaulinleMalin@gmail.com", [], [], 100
    )

    assert str(utilisateur) == "Joueur(TestUser"


def test_utilisateur_modification():
    utilisateur = Utilisateur(
        "CamillelaChenille", "password123", "CamillelaChenille@gmail.com", [], [], 100
    )

    # Modification des points
    utilisateur.points += 50
    assert utilisateur.points == 150

    # Modification des paris
    utilisateur.paris.append(Pari("Nouveau Paris"))
    assert len(utilisateur.paris) == 1
    assert utilisateur.paris[0].nom == "Nouveau Paris"


def test_nom_utilisateur_type():
    """Test que nom_utilisateur doit être un str"""
    pari_test = Pari(1, 2, 3, 4, 1.5, "en cours", 100.0)
    with pytest.raises(TypeError, match="nom_utilisateur doit être de type str"):
        Utilisateur(123, "blipblup123", "blip@gmail.com", [], pari_test, 100)


def test_mot_de_passe_type():
    """Test que mot_de_passe doit être un str"""
    pari_test = Pari(1, 2, 3, 4, 1.5, "en cours", 100.0)
    with pytest.raises(TypeError, match="mot_de_passe doit être de type str"):
        Utilisateur("Rory", 123, "gilmore@gmail.com", [], pari_test, 100)


def test_email_type():
    """Test que email doit être un str"""
    pari_test = Pari(1, 2, 3, 4, 1.5, "en cours", 100.0)
    with pytest.raises(TypeError, match="email doit être de type str"):
        Utilisateur("Zorglub", "strongmdp", 123, [], pari_test, 100)


def test_tournois_crees_type():
    """Test que tournois_crees doit être une liste"""
    pari_test = Pari(1, 2, 3, 4, 1.5, "en cours", 100.0)
    with pytest.raises(TypeError, match="tournois_crees doit être de type list"):
        Utilisateur(
            "monpetitponey", "password123", "poney@example.com", "not a list", pari_test, 100
        )


def test_paris_type():
    """Test que paris doit être un objet de type Pari"""
    with pytest.raises(TypeError, match="paris doit être de type Pari"):
        Utilisateur("john_doe", "password123", "john@example.com", [], "not a Pari", 100)


def test_points_type():
    """Test que points doit être un int"""
    pari_test = Pari(1, 2, 3, 4, 1.5, "en cours", 100.0)
    with pytest.raises(TypeError, match="points doit être de type int"):
        Utilisateur("john_doe", "password123", "john@example.com", [], pari_test, "not an int")
