from unittest.mock import MagicMock

from service.utilisateur_service import UtilisateurService

from dao.utilisateur_dao import UtilisateurDao

from business_object.utilisateur import Utilisateur


liste_utilisateurs = [
    Utilisateur(pseudo="jp", age="10", mail="jp@mail.fr", mdp="1234"),
    Utilisateur(pseudo="lea", age="10", mail="lea@mail.fr", mdp="0000"),
    Utilisateur(pseudo="gg", age="10", mail="gg@mail.fr", mdp="abcd"),
]


def test_creer_ok():
    """ "Création de Utilisateur réussie"""

    # GIVEN
    pseudo, mdp, age, mail, fan_pokemon = "jp", "1234", 15, "z@mail.oo", True
    utilisateurDao().creer = MagicMock(return_value=True)

    # WHEN
    utilisateur = UtilisateurService().creer(pseudo, mdp, age, mail, fan_pokemon)

    # THEN
    assert utilisateur.pseudo == pseudo


def test_creer_echec():
    """Création de Utilisateur échouée
    (car la méthode UtilisateurDao().creer retourne False)"""

    # GIVEN
    pseudo, mdp, age, mail, fan_pokemon = "jp", "1234", 15, "z@mail.oo", True
    UtilisateurDao().creer = MagicMock(return_value=False)

    # WHEN
    utilisateur = UtilisateurService().creer(pseudo, mdp, age, mail, fan_pokemon)

    # THEN
    assert utilisateur is None


def test_lister_tous_inclure_mdp_true():
    """Lister les Utilisateurs en incluant les mots de passe"""

    # GIVEN
    UtilisateurDao().lister_tous = MagicMock(return_value=liste_utilisateurs)

    # WHEN
    res = UtilisateurService().lister_tous(inclure_mdp=True)

    # THEN
    assert len(res) == 3
    for utilisateur in res:
        assert utilisateur.mdp is not None


def test_lister_tous_inclure_mdp_false():
    """Lister les Utilisateurs en excluant les mots de passe"""

    # GIVEN
    UtilisateurDao().lister_tous = MagicMock(return_value=liste_utilisateurs)

    # WHEN
    res = UtilisateurService().lister_tous()

    # THEN
    assert len(res) == 3
    for utilisateur in res:
        assert not utilisateur.mdp


def test_pseudo_deja_utilise_oui():
    """Le pseudo est déjà utilisé dans liste_utilisateurs"""

    # GIVEN
    pseudo = "lea"

    # WHEN
    UtilisateurDao().lister_tous = MagicMock(return_value=liste_utilisateurs)
    res = UtilisateurService().pseudo_deja_utilise(pseudo)

    # THEN
    assert res


def test_pseudo_deja_utilise_non():
    """Le pseudo n'est pas utilisé dans liste_utilisateurs"""

    # GIVEN
    pseudo = "chaton"

    # WHEN
    UtilisateurDao().lister_tous = MagicMock(return_value=liste_utilisateurs)
    res = UtilisateurService().pseudo_deja_utilise(pseudo)

    # THEN
    assert not res


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
