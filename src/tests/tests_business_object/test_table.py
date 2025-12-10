"""Implémentation des tests pour la classe Table"""

import pytest

from business_object.table import Table


class TestTable:
    def test_table_len_succes(self):
        # GIVEN
        table = Table(8, 40)
        taille_attendu = 0

        # WHEN
        taille = len(table)

        # THEN
        assert taille == taille_attendu

    def test_table_ajoute_joueur_succes(self):
        # GIVEN
        table = Table(10, 10)
        id_joueur = 1
        liste_id_joueurs = [1]

        # WHEN
        table.ajouter_joueur(id_joueur)

        # THEN
        assert len(table) == 1
        assert table.id_joueurs == liste_id_joueurs

    def test_table_ajouter_joueur_type_incorrecte(self):
        # GIVEN
        id_joueur = "1"
        table = Table(1, 10, 1, [])
        message_attendu = f"L'id_joueur n'est pas un entier : {type(id_joueur)}"

        # WHEN / THEN
        with pytest.raises(TypeError, match=message_attendu):
            table.ajouter_joueur(id_joueur)

    def test_table_ajouter_joueur_table_pleine(self):
        # GIVEN
        id_joueur = 1
        table = Table(2, 10, id_joueurs=[2, 3])
        message_attendu = "Nombre maximum de joueurs atteint"

        # WHEN / THEN
        with pytest.raises(ValueError, match=message_attendu):
            table.ajouter_joueur(id_joueur)

    def test_table_retirer_joueur_succes(self):
        # GIVEN
        index = 0
        table = Table(10, 10, id_joueurs=[1])
        table_attendu = Table(10, 10, id_joueurs=[])
        # THEN
        id_joueur_supprime = table.retirer_joueur(index)
        # WHEN
        assert len(table) == len(table_attendu)
        assert table.id_joueurs == table_attendu.id_joueurs
        assert id_joueur_supprime == 1

    def test_table_retirer_joueur_valeur_incorrecte(self):
        # GIVEN
        table = Table(1, 10, 1, id_joueurs=[1])
        # WHEN
        with pytest.raises(IndexError, match="Indice plus grand que le nombre de joueurs"):
            table.retirer_joueur(5)

        with pytest.raises(IndexError, match="Indice négatif impossible"):
            table.retirer_joueur(-1)

    def test_table_retirer_joueur_valeur_incorrecte2(self):
        # GIVEN
        table = Table(1, 10, 1, id_joueurs=[1])
        index = 5
        # WHEN/THEN
        with pytest.raises(IndexError, match="Indice plus grand que le nombre de joueurs"):
            table.retirer_joueur(index)

    def test_table_retirer_joueur_valeur_incorrecte3(self):
        # GIVEN
        table = Table(1, 10, 1, id_joueurs=[1])
        message_attendu = "L'indice doit être un entier"
        id_joueurs = "a"

        # WHEN / THEN
        with pytest.raises(TypeError, match=message_attendu):
            table.retirer_joueur(id_joueurs)

    def test_table_mettre_grosse_blind_succes(self):
        # GIVEN
        table = Table(10, 10, 1)
        credit = 50

        # WHEN
        table.mettre_grosse_blind(credit)

        # THEN
        assert table.grosse_blind == credit

    def test_table_mettre_grosse_blind_valeur_incorrecte3(self):
        # GIVEN
        table = Table(1, 10, 1)
        message_attendu = "Le crédit doit être un int"
        credit = "a"

        # WHEN / THEN
        with pytest.raises(TypeError, match=message_attendu):
            table.mettre_grosse_blind(credit)

    def test_table_rotation_dealer_succes(self):
        # GIVEN
        id_joueur1 = 1
        id_joueur2 = 2
        table = Table(2, 2, id_joueurs=[id_joueur1, id_joueur2])
        table_attendue = Table(2, 2, id_joueurs=[id_joueur2, id_joueur1])

        # WHEN
        table.rotation_dealer()

        # THEN
        assert table.id_joueurs == table_attendue.id_joueurs

    def test_table_lancer_manche_succes(self):
        # GIVEN

        # WHEN

        # THEN
        assert True
