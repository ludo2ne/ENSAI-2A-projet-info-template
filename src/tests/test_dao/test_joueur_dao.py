import os
import pytest

from unittest.mock import patch

from utils.reset_database import ResetDatabase
from utils.securite import hash_password

from dao.utilisateur_dao import UtilisateurDao

from business_object.utilisateur import Utilisateur


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialisation des données de test"""
    with patch.dict(os.environ, {"SCHEMA": "projet_test_dao"}):
        ResetDatabase().lancer(test_dao=True)
        yield


def test_trouver_par_id_existant():
    """Recherche par id d'un utilisateur existant"""

    # GIVEN
    id_utilisateur = 998

    # WHEN
    utilisateur = UtilisateurDao().trouver_par_id(id_utilisateur)

    # THEN
    assert utilisateur is not None


def test_trouver_par_id_non_existant():
    """Recherche par id d'un utilisateur n'existant pas"""

    # GIVEN
    id_utilisateur = 9999999999999

    # WHEN
    utilisateur = UtilisateurDao().trouver_par_id(id_utilisateur)

    # THEN
    assert utilisateur is None


def test_lister_tous():
    """Vérifie que la méthode renvoie une liste de Utilisateur
    de taille supérieure ou égale à 2
    """

    # GIVEN

    # WHEN
    utilisateurs = UtilisateurDao().lister_tous()

    # THEN
    assert isinstance(utilisateurs, list)
    for j in utilisateurs:
        assert isinstance(j, Utilisateur)
    assert len(utilisateurs) >= 2


def test_creer_ok():
    """Création de Utilisateur réussie"""

    # GIVEN
    utilisateur = Utilisateur(pseudo="gg", age=44, mail="test@test.io")

    # WHEN
    creation_ok = UtilisateurDao().creer(utilisateur)

    # THEN
    assert creation_ok
    assert utilisateur.id_utilisateur


def test_creer_ko():
    """Création de Utilisateur échouée (age et mail incorrects)"""

    # GIVEN
    utilisateur = Utilisateur(pseudo="gg", age="chaine de caractere", mail=12)

    # WHEN
    creation_ok = UtilisateurDao().creer(utilisateur)

    # THEN
    assert not creation_ok


def test_modifier_ok():
    """Modification de Utilisateur réussie"""

    # GIVEN
    new_mail = "maurice@mail.com"
    utilisateur = Utilisateur(id_utilisateur=997, pseudo="maurice", age=20, mail=new_mail)

    # WHEN
    modification_ok = UtilisateurDao().modifier(utilisateur)

    # THEN
    assert modification_ok


def test_modifier_ko():
    """Modification de Utilisateur échouée (id inconnu)"""

    # GIVEN
    utilisateur = Utilisateur(id_utilisateur=8888, pseudo="id inconnu", age=1, mail="no@mail.com")

    # WHEN
    modification_ok = UtilisateurDao().modifier(utilisateur)

    # THEN
    assert not modification_ok


def test_supprimer_ok():
    """Suppression de Utilisateur réussie"""

    # GIVEN
    utilisateur = Utilisateur(id_utilisateur=995, pseudo="miguel", age=1, mail="miguel@projet.fr")

    # WHEN
    suppression_ok = UtilisateurDao().supprimer(utilisateur)

    # THEN
    assert suppression_ok


def test_supprimer_ko():
    """Suppression de Utilisateur échouée (id inconnu)"""

    # GIVEN
    utilisateur = Utilisateur(id_utilisateur=8888, pseudo="id inconnu", age=1, mail="no@z.fr")

    # WHEN
    suppression_ok = UtilisateurDao().supprimer(utilisateur)

    # THEN
    assert not suppression_ok


def test_se_connecter_ok():
    """Connexion de Utilisateur réussie"""

    # GIVEN
    pseudo = "batricia"
    mdp = "9876"

    # WHEN
    utilisateur = UtilisateurDao().se_connecter(pseudo, hash_password(mdp, pseudo))

    # THEN
    assert isinstance(utilisateur, utilisateur)


def test_se_connecter_ko():
    """Connexion de Utilisateur échouée (pseudo ou mdp incorrect)"""

    # GIVEN
    pseudo = "toto"
    mdp = "poiuytreza"

    # WHEN
    utilisateur = UtilisateurDao().se_connecter(pseudo, hash_password(mdp, pseudo))

    # THEN
    assert not utilisateur


if __name__ == "__main__":
    pytest.main([__file__])
