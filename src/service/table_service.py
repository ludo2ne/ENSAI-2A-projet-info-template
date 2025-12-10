"""Implémentation de la classe TableService"""

from business_object.table import Table
from service.credit_service import CreditService
from service.joueur_service import JoueurService
from service.manche_joueur_service import MancheJoueurService
from service.manche_service import MancheService
from utils.log_decorator import log


class TableService:
    """
    Service métier pour la gestion des tables de poker :
    - Création, suppression et consultation des tables
    - Gestion des joueurs à l’intérieur des tables
    - Gestion du déroulement des manches
    """

    __tables: list[Table] = []
    compteur_tables: int = 0

    def liste_tables(self) -> list[Table]:
        """Liste l'ensemble des tables disponibles"""
        return self.__tables

    def affichages_tables(self) -> list[str]:
        """Affichage de l'ensemble des tables créées"""
        return [str(table) for table in self.__tables]

    def table_par_affichage(self, affichage: str) -> Table:
        """Renvoie la table correspondante à l'affichage"""
        indice_table = self.affichages_tables().index(affichage)
        return self.__tables[indice_table]

    def table_par_numero(self, numero_table: int) -> Table:
        """
        Renvoie la table correspondant au numéro si elle existe

        Paramètres
        ----------
        numero_table : int
            le numéro de la table recherchée

        Renvois
        -------
        Table
            la table recherchée si elle existe

        Exceptions
        ----------
        ValueError
            si aucune table n'est trouvée avec ce numéro
        """

        for table in self.__tables:
            print(table.numero_table)
            if table.numero_table == numero_table:
                return table

        raise ValueError(f"Aucune table existante ne porte le numéro {numero_table}")

    @log
    def creer_table(self, joueurs_max: int, grosse_blind: int, mode_jeu: int = 1) -> Table:
        """
        Créer une table de jeu de poker

        Paramètres
        ----------
        joueur_max : int
            le nombre de joueurs maximum que la table peut accueillir
        hrosse_blind : int
            la valeur de la grosse blind
        mode_jeu : int
            le code du mode de jeu de la table

        Renvois
        -------
        Table
            la table créée
        """

        self.compteur_tables += 1
        numero = self.compteur_tables

        table = Table(
            numero_table=numero,
            joueurs_max=joueurs_max,
            grosse_blind=grosse_blind,
            mode_jeu=mode_jeu,
        )

        self.__tables.append(table)
        return table

    @log
    def supprimer_table(self, numero_table: int) -> None:
        """
        Supprime une table

        Paramètres
        ----------
        numero_table : int
            le numéro de la table à supprimer

        Renvois
        -------
        None
        """

        table = self.table_par_numero(numero_table)

        for joueur in list(table.joueurs):
            joueur.quitter_table()
        if table in self.__tables:
            self.__tables.remove(table)

    @log
    def ajouter_joueur(self, numero_table: int, id_joueur: int) -> None:
        """
        Ajoute un joeuur à une table

        Paramètres
        ----------
        numero_table : int
            le numéro de la table où ajouter un joueur
        id_joueur : int
            l'identifiant du joueur à ajouter à la table

        Renvois
        -------
        None
        """

        joueur = JoueurService().trouver_par_id(id_joueur)

        if not joueur:
            raise ValueError(f"Le joueur avec l'identifiant {id_joueur} n'existe pas")
        if joueur.numero_table is not None:
            raise ValueError("Le joueur est déjà à une table")

        table = self.table_par_numero(numero_table)

        joueur_dans_table = False

        try:
            table.ajouter_joueur(id_joueur)
            joueur_dans_table = True
            joueur.rejoindre_table(numero_table)
        except Exception as e:
            if joueur_dans_table:
                table.retirer_joueur(id_joueur)

            raise Exception(f"Échec, {joueur.pseudo} n'a pas rejoint la table {numero_table} : {e}")

        JoueurService().maj_joueur(joueur)

    @log
    def retirer_joueur(self, id_joueur: int) -> None:
        """
        Ajoute un joeuur à une table

        Paramètres
        ----------
        id_joueur : int
            l'identifiant du joueur à retirer de sa table

        Renvois
        -------
        None
        """

        joueur = JoueurService().trouver_par_id(id_joueur)
        table = TableService().table_par_numero(joueur.numero_table)

        joueur.quitter_table()
        table.retirer_joueur(table.id_joueurs.index(id_joueur))

    @log
    def lancer_manche(self, numero_table: int) -> None:
        """
        Ajoute un joeuur à une table

        Paramètres
        ----------
        numero_table : int
            le numéro de la table où lancer la manche

        Renvois
        -------
        None
        """

        table = self.table_par_numero(numero_table)
        if table.manche is None or table.manche.fin:
            pseudos = []

            for id in range(len(table)):
                joueur = JoueurService().trouver_par_id(table.id_joueurs[id])
                if joueur.credit < table.grosse_blind:
                    self.retirer_joueur(joueur.id_joueur)
                else:
                    pseudos.append(joueur.pseudo)

            table.nouvelle_manche(pseudos)
            table.manche.preflop()
            p_blind = table.manche.info.joueurs[0]
            g_blind = table.manche.info.joueurs[1]

            grosse_blind = table.manche.grosse_blind

            from service.action_service import ActionService

            ActionService().suivre(p_blind, grosse_blind // 2)
            ActionService().suivre(g_blind, grosse_blind - grosse_blind // 2)
            table.manche.info.modifier_statut(1, 0)

    def affichage_general(self, numero_table: int) -> str:
        """
        Affiche la main d'un joueur

        Paramètres
        ----------
        numero_table : int
            le numéro de la table où le joueur se trouve
        id_joueur : int
            le joueur qui souhaite regarder sa main

        Renvois
        -------
        str
            les cartes de la main du joueur
        """

        table = self.table_par_numero(numero_table)

        return table.manche.affichage_complet()

    def regarder_main(self, id_joueur: int) -> str:
        """
        Affiche la main d'un joueur

        Paramètres
        ----------
        numero_table : int
            le numéro de la table où le joueur se trouve
        id_joueur : int
            le joueur qui souhaite regarder sa main

        Renvois
        -------
        str
            les cartes de la main du joueur
        """

        joueur = JoueurService().trouver_par_id(id_joueur)
        numero_table = joueur.numero_table
        table = self.table_par_numero(numero_table)

        return table.manche.regarder_cartes(id_joueur)

    @log
    def terminer_manche(self, numero_table: int) -> str:
        """
        Ajoute un joeuur à une table

        Paramètres
        ----------
        numero_table : int
            le numéro de la table où lancer la manche

        Renvois
        -------
        None
        """

        table = self.table_par_numero(numero_table)

        gains = table.manche.terminer_manche()

        if gains is not None:
            for id_joueur, montant in gains.items():
                joueur = JoueurService().trouver_par_id(id_joueur)
                CreditService().crediter(joueur, montant)

            id_manche = MancheService().sauvegarder_manche(table.manche)
            MancheJoueurService().sauvegarder_manche_joueur(id_manche, table.manche.info, gains)
            table.rotation_dealer()

        return table.manche.resultats()
