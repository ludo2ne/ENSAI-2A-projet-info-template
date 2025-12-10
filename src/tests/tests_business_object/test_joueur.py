"""Implémentation des tests pour la classe Joueur"""

import pytest

from business_object.joueur import Joueur


class TestJoueur:
    @pytest.fixture
    def joueur(self):
        return Joueur(1, "Pikachu", 100, "France")

    @pytest.fixture
    def joueur_en_jeu(self):
        return Joueur(1, "Pikachu", 100, "France", 1)

    def test_joueur_init_succes(self):
        # GIVEN
        id_joueur = 1
        pseudo = "Pikachu"
        credit = 100
        pays = "France"

        # WHEN
        joueur = Joueur(id_joueur, pseudo, credit, pays)

        # THEN
        assert joueur.id_joueur == 1
        assert joueur.pseudo == "Pikachu"
        assert joueur.credit == 100
        assert joueur.pays == "France"
        assert joueur.numero_table is None

    @pytest.mark.parametrize(
        "id_joueur, pseudo, credit, pays",
        [
            ("1", "Pikachu", 200, "France"),
            (1, False, 200, "France"),
            (1, "Pikachu", "200", "France"),
            (1, "Pikachu", 200, True),
        ],
    )
    def test_joueur_init_TypeError(self, id_joueur, pseudo, credit, pays):
        # GIVEN
        # paramètres injectés par parametrize

        # WHEN / THEN
        with pytest.raises(TypeError):
            Joueur(id_joueur, pseudo, credit, pays)

    @pytest.mark.parametrize(
        "id_joueur, pseudo, credit, pays",
        [
            (0, "Pikachu", 200, "France"),
            (1, "Pikachu", -200, "France"),
        ],
    )
    def test_joueur_init_ValueError(self, id_joueur, pseudo, credit, pays):
        # GIVEN
        # paramètres injectés par parametrize

        # WHEN / THEN
        with pytest.raises(ValueError):
            Joueur(id_joueur, pseudo, credit, pays)

    def test_joueur_str(self, joueur):
        # GIVEN
        resultat = "Pikachu : 100 crédits"

        # WHEN
        affichage = str(joueur)

        # THEN
        assert affichage == resultat

    @pytest.mark.parametrize(
        "joueur1, joueur2, resultat",
        [
            (Joueur(1, "Crocorible", 200, "France"), Joueur(1, "Crocorible", 200, "France"), True),
            (Joueur(1, "Crocorible", 200, "France"), Joueur(2, "Pikachu", 200, "France"), False),
            (Joueur(1, "Crocorible", 200, "France"), "pas un joueur", False),
        ],
    )
    def test_joueur_eq(self, joueur1, joueur2, resultat):
        # GIVEN
        # paramètres injectés par parametrize

        # WHEN / THEN
        assert (joueur1 == joueur2) is resultat

    def test_joueur_ajouter_credits_succes(self, joueur):
        # GIVEN
        credits = 50

        # WHEN
        joueur.ajouter_credits(credits)

        # THEN
        assert joueur.credit == 150

    def test_joueur_ajouter_credits_TypeError(self, joueur):
        # GIVEN
        credits = "50"
        message_attendu = f"Les crédits doivent être de type int : {type(credits)}"

        # WHEN
        with pytest.raises(TypeError, match=message_attendu):
            joueur.ajouter_credits(credits)

    def test_joueur_ajouter_credits_ValueError(self, joueur):
        # GIVEN
        credits = -50
        message_attendu = f"Le nombre de crédits à ajouter doit être positif : {credits}"

        # WHEN
        with pytest.raises(ValueError, match=message_attendu):
            joueur.ajouter_credits(credits)

    def test_joueur_retirer_credits_succes(self, joueur):
        # GIVEN
        credits = 50

        # WHEN
        joueur.retirer_credits(credits)

        # THEN
        assert joueur.credit == 50

    def test_joueur_retirer_credits_echec_pas_int(self, joueur):
        # GIVEN
        credits = "50"
        message_attendu = f"Les crédits doivent être de type int : {type(credits)}"

        # WHEN / THEN
        with pytest.raises(TypeError, match=message_attendu):
            joueur.retirer_credits(credits)

    def test_joueur_retirer_credits_echec_credits_negatifs(self, joueur):
        # GIVEN
        credits = -50
        message_attendu = f"Le nombre de crédits à retirer doit être positif : {credits}"

        # WHEN / THEN
        with pytest.raises(ValueError, match=message_attendu):
            joueur.retirer_credits(credits)

    def test_joueur_retirer_credits_echec_credits_insuffisants(self, joueur):
        # GIVEN
        credits = 200
        message_attendu = f"Le joueur {joueur.pseudo} a trop peu de crédits pour retirer {credits}: {joueur.credit}"

        # WHEN / THEN
        with pytest.raises(ValueError, match=message_attendu):
            joueur.retirer_credits(credits)

    def test_joueur_rejoindre_table_succes(self, joueur):
        # GIVEN
        numero_table = 1

        # WHEN
        joueur.rejoindre_table(numero_table)

        # THEN
        assert joueur.numero_table == numero_table

    def test_joueur_rejoindre_table_echec_deja_en_jeu(self, joueur_en_jeu):
        # GIVEN
        numero_table = 2
        message_attendu = f"Le joueur {joueur_en_jeu.pseudo} est déjà à une table"

        # WHEN / THEN
        with pytest.raises(Exception, match=message_attendu):
            joueur_en_jeu.rejoindre_table(numero_table)

    def test_joueur_rejoindre_table_echec_mauvais_type_table(self, joueur):
        # GIVEN
        numero_table = "2"
        message_attendu = f"le paramètre numero_table doit être un int : {type(numero_table)}"

        # WHEN / THEN
        with pytest.raises(TypeError, match=message_attendu):
            joueur.rejoindre_table(numero_table)

    def test_joueur_quitter_table_succes(self, joueur_en_jeu):
        # GIVEN
        joueur_en_jeu

        # WHEN
        joueur_en_jeu.quitter_table()

        # THEN
        assert joueur_en_jeu.numero_table is None

    def test_joueur_quitter_table_echec_aucune_table(self, joueur):
        # GIVEN
        message_attendu = f"Le joueur {joueur.pseudo} n'est actuellement à aucune table"

        # WHEN / THEN
        with pytest.raises(Exception, match=message_attendu):
            joueur.quitter_table()

    def test_joueur_changer_pseudo_succes(self, joueur):
        # GIVEN
        nouveau_pseudo = "Raichu"

        # WHEN
        joueur.changer_pseudo(nouveau_pseudo)

        # THEN
        assert joueur.pseudo == "Raichu"

    def test_joueur_changer_pseudo_TypeError(self, joueur):
        # GIVEN
        nouveau_pseudo = 123
        msg = f"Le pseudo doit être de type str : {type(nouveau_pseudo)}"

        # WHEN / THEN
        with pytest.raises(TypeError, match=msg):
            joueur.changer_pseudo(nouveau_pseudo)

    def test_joueur_changer_pays_succes(self, joueur):
        # GIVEN
        nouveau_pays = "Japon"

        # WHEN
        joueur.changer_pays(nouveau_pays)

        # THEN
        assert joueur.pays == "Japon"

    def test_joueur_changer_pays_TypeError(self, joueur):
        # GIVEN
        nouveau_pays = 42
        msg = f"Le pays doit être de type str : {type(nouveau_pays)}"

        # WHEN / THEN
        with pytest.raises(TypeError, match=msg):
            joueur.changer_pays(nouveau_pays)
