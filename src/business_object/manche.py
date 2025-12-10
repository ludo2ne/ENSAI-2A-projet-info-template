"""Implémentation de la classe Manche"""

from business_object.board import Board
from business_object.evaluateur_combinaison import EvaluateurCombinaison
from business_object.info_manche import InfoManche
from business_object.reserve import Reserve
from utils.log_decorator import log


class Manche:
    """Modélise une manche complète de poker"""

    __TOURS = ("preflop", "flop", "turn", "river")

    def __init__(self, info: InfoManche, grosse_blind: int):
        """
        Initialise une manche de poker.

        Paramètres
        ----------
        info : InfoManche
            Informations sur les joueurs et leurs mains
        grosse_blind : int
            Montant de la grosse blind, qui doit être > 2

        Exceptions
        ----------
        TypeError
            si info n'est pas une InfoManche ou grosse_blind n'est pas un int
        ValueError
            si grosse_blind < 2
        """

        if not isinstance(info, InfoManche):
            raise TypeError(
                f"Le paramètre 'info' doit être une instance de InfoManche, pas {type(info).__name__}."
            )

        if not isinstance(grosse_blind, int):
            raise TypeError(
                f"Le paramètre 'grosse_blind' doit être un entier, pas {type(grosse_blind).__name__}."
            )

        if grosse_blind < 2:
            raise ValueError("Le montant de la grosse blind doit être supérieur à 2")

        self.__tour = 0
        self.__info = info
        self.__reserve = Reserve(None)
        self.__board = Board([])
        self.__indice_joueur_actuel = 0
        self.__grosse_blind = grosse_blind
        self.__fin = False
        self.__enregistree = False

    @property
    def tour(self) -> int:
        """Renvoie le tour de jeu actuel"""
        return self.__tour

    @tour.setter
    def tour(self, value: int):
        """Modifie le tour de jeu pour la progression de la manche"""
        if not isinstance(value, int) or not (0 <= value <= 3):
            raise ValueError("Le tour doit être un entier entre 0 et 3")
        self.__tour = value

    @property
    def info(self) -> InfoManche:
        """Retourne les informations des joueurs dans la manchee"""
        return self.__info

    @property
    def reserve(self) -> Reserve:
        """Paquet de carte constituant la pioche"""
        return self.__reserve

    @property
    def board(self) -> Board:
        """Retourne les cartes communes visibles sur la table"""
        return self.__board

    @property
    def indice_joueur_actuel(self) -> int:
        """Renvoie l'indice du joueur dont c'est le tour"""
        return self.__indice_joueur_actuel

    @property
    def grosse_blind(self) -> int:
        """Renvoie la valeur de la grosse blind"""
        return self.__grosse_blind

    @property
    def fin(self) -> bool:
        """Indique si la manche est terminée"""
        return self.__fin

    @classmethod
    def TOURS(cls) -> tuple:
        """Liste des phases de jeu d'une manche de poker"""
        return cls.__TOURS

    def __str__(self) -> str:
        """Représentation informelle d'un objet de type 'Manche'"""
        return f"Manche(tour={self.TOURS()[self.tour]}, grosse_blind={self.grosse_blind}, board={self.board})"

    def __repr__(self) -> str:
        """Représentation informelle d'un objet de type 'Manche'"""
        return f"Manche(tour={self.TOURS()[self.tour]}, grosse_blind={self.grosse_blind}, board={self.board})"

    def affichage_complet(self) -> str:
        """Représentation des informations globales de la manche"""

        tour = f"｡.｡:+* ﾟ ゜ﾟ *+:｡.｡:+* ﾟ ゜ﾟ *+:｡.｡.｡:+[ {self.TOURS()[self.tour]} ]+:｡.｡:+* ﾟ ゜ﾟ *+:｡.｡.｡:+* ﾟ ゜ﾟ *+:｡.｡\n\n"
        info = self.info.affichage_tout_joueur() + "\n\n\n"
        board = "Board :" + self.board.affichage_board() + "\n\n"
        if self.fin:
            instruction = "La manche est terminée !"
        else:
            instruction = f"C'est à {self.info.pseudos[self.indice_joueur_actuel]} de jouer !"

        return tour + info + board + instruction

    def indice_joueur(self, id_joueur: int) -> int:
        """
        Retourne l'indice du joueur si il est présent dans la manche

        Paramètres
        ----------
        joueur : Joueur
            Le joueur recherché dans la manche

        Renvois
        -------
        int
            l'indice du joueur dans InfoManche

        Exceptions
        ----------
        ValueError
            si le joueur n'est pas présent dans la manche
        """

        for i in range(len(self.info.joueurs)):
            if self.info.joueurs[i] == id_joueur:
                return i
        raise ValueError("Le joueur n'est pas dans cette manche")

    def regarder_cartes(self, id_joueur: int) -> str:
        """
        Renvoie les cartes d'un joeuur au format texte

        Paramètres
        ----------
        joueur : Joueur
            joueur dont on veut renvoyer la main

        Renvois
        -------
        str
            les cartes du joeuur
        """

        indice = self.indice_joueur(id_joueur)
        if self.info.mains[indice] is None:
            return "   [?]      [?]   "
        else:
            return self.info.mains[indice].affichage_main()

    def est_tour(self, id_joueur: int) -> bool:
        """
        Vérifie si c'est au tour du joueur

        Paramètres
        ----------
        joueur : Joueur
            joueur dont on veut vérifier si c'est le tour

        Renvois
        -------
        bool
            True si c'est bien au tour du joueur, False sinon
        """

        return self.indice_joueur_actuel == self.indice_joueur(id_joueur)

    def indice_joueur_suivant(self) -> int:
        """
        Retourne l'indice du joueur suivant à qui c'est le tour de jouer

        Paramètres
        ----------
        None

        Renvois
        -------
        int
            indice du prochain joueur actif

        Exceptions
        ----------
        ValueError
            si tous les jouers sont couchés
        """

        if all(s == 3 for s in self.info.statuts):
            raise ValueError("Tous les joueurs ne peuvent être couchés")

        indice = self.indice_joueur_actuel
        statuts = self.info.statuts

        if indice == len(statuts) - 1:
            indice = 0
        else:
            indice += 1

        while statuts[indice] in [3, 4]:
            if indice == len(statuts) - 1:
                indice = 0
            else:
                indice += 1

        return indice

    def joueur_suivant(self) -> None:
        """Passe au tour du joueur actif suivant"""
        self.__indice_joueur_actuel = self.indice_joueur_suivant()

    def indice_nouveau_tour(self):
        """Donne la main au joueur après le dealer encore en jeu"""
        self.__indice_joueur_actuel = len(self.info.joueurs) - 1
        self.joueur_suivant()

    def statuts_nouveau_tour(self):
        """Met à jour les statuts des joueurs pour un nouveau tour"""
        for i in range(len(self.info.statuts)):
            if self.info.statuts[i] not in [3, 4]:
                self.info.modifier_statut(i, 0)

    def nouveau_tour(self):
        """Passe à la phase suivante et met à jour les statuts des joueurs"""
        if self.tour == 3:
            raise ValueError("La manche est déjà au dernier tour")
        self.__tour += 1
        self.indice_nouveau_tour()
        self.statuts_nouveau_tour()

    @log
    def preflop(self):
        """Distribution des cartes initiales et mise des blinds"""
        self.reserve.melanger()
        self.info.assignation_mains(self.reserve.distribuer(len(self.info.joueurs)))

    @log
    def flop(self) -> str:
        """Révélation des 3 premières cartes communes"""
        self.__reserve.bruler()
        for _ in range(3):
            self.__reserve.reveler(self.__board)
        self.nouveau_tour()
        return "La phase de flop commence !"

    @log
    def turn(self) -> str:
        """Révélation de la quatrième carte commune"""
        self.__reserve.bruler()
        self.__reserve.reveler(self.__board)
        self.nouveau_tour()
        return "La phase de turn commence !"

    @log
    def river(self) -> str:
        """Révélation de la cinquième carte commune"""
        self.__reserve.bruler()
        self.__reserve.reveler(self.__board)
        self.nouveau_tour()
        return "La phase de river commence !"

    def fin_du_tour(self) -> bool:
        """Vérifie si tous les joueurs ont égalisé / couché / All-in"""
        return all(s not in [0, 1] for s in self.info.statuts)

    def fin_de_manche(self) -> bool:
        """Vérifie si la manche est terminée"""
        n = sum(1 for s in self.info.statuts if s != 3)
        n_all = sum(1 for s in self.info.statuts if s == 4)
        n_late = sum(1 for s in self.info.statuts if s == 1)
        if n == 0:
            raise ValueError("Les joueurs ne peuvent être tous couchés")
        return (
            n_all == len(self.joueurs_en_lice)
            or (n_all == len(self.joueurs_en_lice) - 1 and n_late == 0)
            or n == 1
            or (self.fin_du_tour() and self.tour == 3)
        )

    @log
    def checker(self, indice_joueur: int):
        """
        Le joueur choisit de ne pas relancer (check) si possible.

        Paramètres
        ----------
        indice_joueur : int
            Indice du joueur

        Exceptions
        ----------
        TypeError
            si indice_joueur n'est pas un int
        ValueError
            si le joueur ne peut pas checker
        """

        if not isinstance(indice_joueur, int):
            raise TypeError("indice_joueur doit être un entier")
        if self.info.statuts[indice_joueur] != 0:
            raise ValueError("Le joueur doit avoir le statut d'innactif pour checker")
        self.info.modifier_statut(indice_joueur, 2)

    @log
    def suivre(self, indice_joueur: int, credit_joueur: int, relance: int = 0) -> int:
        """
        Permet à un joueur de suivre ou relancer.

        Paramètres
        ----------
        indice_joueur : int
            Indice du joueur
        credit_joueur : int
            Les crédits du joueur qui veut suivre
        relance : int
            Montant de la relance additionnelle

        Retour
        ------
        int
            Montant total misé par le joueur ce tour

        Exceptions
        ----------
        TypeError, ValueError
            si paramètres invalides
        """

        if not isinstance(indice_joueur, int):
            raise TypeError("indice_joueur doit être un entier")
        if not isinstance(relance, int) or relance < 0:
            raise ValueError("Le montant doit être un entier positif")

        if relance == 0 and self.info.statuts[indice_joueur] == 0:
            raise ValueError(
                "Vous ne pouvez pas suivre alors que vous êtes déjà à jour, il faut checker."
            )

        pour_suivre = max(self.info.mises) - self.info.mises[indice_joueur]

        if pour_suivre >= credit_joueur:
            raise ValueError("Le joueur doit all-in")
        if relance + pour_suivre >= credit_joueur:
            raise ValueError("Le joueur ne peut relancer autant")

        ancienne_mise = self.info.mises[indice_joueur]
        nouvelle_mise = pour_suivre + relance + ancienne_mise
        self.info.modifier_mise(indice_joueur, nouvelle_mise)
        self.info.modifier_statut(indice_joueur, 2)

        if relance > 0:
            for i in range(len(self.info.statuts)):
                if i != indice_joueur and self.info.statuts[i] in [0, 2]:
                    self.info.statuts[i] = 1

        return pour_suivre + relance

    @log
    def all_in(self, indice_joueur: int, credit_joueur: int) -> int:
        """
        Mise tout le crédit d'un joueur

        Paramètres
        ----------
        indice_joueur : int
            l'indice du joueur qui all-in
        credit_joueur : int
            Les crédits du joueur qui veut suivre

        Renvois
        -------
        int
            la somme totale misée pour all-in

        Exceptions
        ----------
        ValueError
            si le joueur est couché ou déjà all-in
        """

        if self.info.statuts[indice_joueur] in [3, 4]:
            raise ValueError("Le joueur ne peut plus all-in")

        montant = credit_joueur
        pour_suivre = max(self.info.mises) - self.info.mises[indice_joueur]

        ancienne_mise = self.info.mises[indice_joueur]
        nouvelle_mise = montant + ancienne_mise
        self.info.modifier_mise(indice_joueur, nouvelle_mise)
        self.info.modifier_statut(indice_joueur, 4)

        if montant > pour_suivre:
            for i in range(len(self.info.statuts)):
                if self.info.statuts[i] in (0, 2):
                    self.info.statuts[i] = 1

        return montant

    @log
    def se_coucher(self, indice_joueur: int) -> None:
        """
        Marque un joueur comme couché  lors de la manche.

        Cette action met à jour :
        - Le tour auquel le joueur s'est couché
        - Le statut du joueur à couché (statut = 3)

        Paramètres
        ----------
        indice_joueur : int
            Indice du joueur dans self.info.joueurs qui souhaite se coucher.

        Renvois
        -------
        None
        """

        self.info.modifier_tour_couche(indice_joueur, self.tour)
        self.info.modifier_statut(indice_joueur, 3)

    def valeur_pot(self) -> int:
        """
        Calcule et retourne la valeur totale du pot de la manche.

        Paramètres
        ----------
        None

        Renvois
        -------
        int
            somme des mises de tous les joueurs
        """

        return sum(self.info.mises)

    @property
    def joueurs_en_lice(self) -> list[int]:
        """
        Renvoie la liste des indices des joueurs encore en lice dans la manche.

        Définition
        ----------
        Joueur en lice : joueur dont le statut n'est pas 'couché' (statut != 3)

        Retour
        ------
        list[int]
            Indices des joueurs actifs.
        """
        return [i for i, statut in enumerate(self.info.statuts) if statut != 3]

    def classement(self) -> list[int]:
        """
        Classe les joueurs selon la force de leur main combinée avec le board.

        Le rang 1 correspond au meilleur joueur. Les ex-aequo reçoivent le même rang.
        Les joueurs non-actifs ou couchés reçoivent le rang 0.

        Paramètres
        ----------
        None

        Renvois
        -------
        list[int]
            Liste des rangs des joueurs (dans l'ordre des joueurs de InfoManche)

        Exceptions
        ----------
        ValueError
            si le board n'est pas complet
        """

        if len(self.board) != 5:
            raise ValueError("Impossible de classer : le board n'est pas complet")

        joueurs_actifs = self.joueurs_en_lice
        evals = {}

        for i in joueurs_actifs:
            cartes_totales = self.info.mains[i].cartes + self.board.cartes
            # On prend la combinaison forcée si elle existe
            if hasattr(self.info.mains[i], "_combinaison") and self.info.mains[i]._combinaison:
                comb = self.info.mains[i]._combinaison
            else:
                comb = EvaluateurCombinaison.eval(cartes_totales)
            evals[i] = comb._valeur_comparaison()

        # Tri décroissant par valeur de combinaison
        sorted_joueurs = sorted(joueurs_actifs, key=lambda i: evals[i], reverse=True)

        classement_dict = {}
        rang = 1
        idx = 0

        while idx < len(sorted_joueurs):
            debut = idx
            # Regroupe les ex-aequo
            while (
                idx + 1 < len(sorted_joueurs)
                and evals[sorted_joueurs[idx + 1]] == evals[sorted_joueurs[debut]]
            ):
                idx += 1
            # Attribuer le même rang à tous les ex-aequo
            for k in range(debut, idx + 1):
                classement_dict[sorted_joueurs[k]] = rang
            # Incrément du rang après les ex-aequo
            rang += idx - debut + 1
            idx += 1

        # Rang pour les joueurs non-actifs (statut != 2)
        for i in range(len(self.info.joueurs)):
            if i not in classement_dict:
                classement_dict[i] = rang

        return [classement_dict[i] for i in range(len(self.info.joueurs))]

    def recuperer(self, mise: int, montant_a_recupere: int) -> list[int]:
        """
        Calcule la répartition d'un montant à récupérer d'une mise.

        Paramètres
        ----------
        mise : int
            Montant total de la mise initiale
        montant_a_recupere : int
            Montant que l'on souhaite récupérer

        Renvois
        ------
        list[int]
            Liste de deux éléments :
            - [0] : montant restant après récupération
            - [1] : montant effectivement récupéré
        """

        if montant_a_recupere >= mise:
            return [0, mise]
        return [mise - montant_a_recupere, montant_a_recupere]

    def gains(self) -> dict:
        """
        Calcule les gains de chaque joueur à la fin de la manche.

        Prend en compte :
        - Les side pots (mises différentes)
        - Les ex-aequo (partage équitable du pot)

        Paramètres
        ----------
        None

        Renvois
        -------
        dict[Joueur, int]
            dictionnaire associant les joueurs en clé à leur gain en value

        Exceptions
        ----------
        ValueError
            si le board n'est pas complet
        """

        if len(self.joueurs_en_lice) == 1:
            gains = {self.info.joueurs[self.joueurs_en_lice[0]]: self.valeur_pot()}
            return gains

        if len(self.board.cartes) != 5 and not self.fin:
            raise ValueError("Le board n'est pas complet, impossible de calculer les gains.")

        # copies / structures locales
        mises_restantes = self.info.mises[:]  # liste modifiable
        classement = self.classement()        # liste des rangs (1 = meilleur, 0 = hors course)
        joueurs = self.info.joueurs           # liste d'objets Joueur
        n = len(joueurs)

        # init gains à 0 (clé : Joueur)
        gains = {j: 0 for j in joueurs}

        # tant qu'il reste de l'argent à distribuer
        while any(m > 0 for m in mises_restantes):
            # participants qui ont contribué à ce round (TOUS ceux avec mise > 0)
            participants_all = [i for i, m in enumerate(mises_restantes) if m > 0]
            if not participants_all:
                break  # sécurité

            # niveau minimal parmi ces participants
            mise_min = min(mises_restantes[i] for i in participants_all)

            # valeur du pot courant (prend mise_min de chaque participant_all)
            pot = sum(min(mises_restantes[i], mise_min) for i in participants_all)

            # retirer la part correspondant à ce niveau
            for i in participants_all:
                prises = min(mises_restantes[i], mise_min)
                mises_restantes[i] -= prises

            # candidats au pot = participants_all
            # mais seuls les joueurs encore en lice peuvent gagner (statut "en lice")
            candidats = [i for i in participants_all if i in self.joueurs_en_lice]

            # s'il n'y a pas de candidat (rare/impossible normalement), on répartit aux contributeurs
            if not candidats:
                candidats = participants_all

            # trouver le meilleur rang parmi les candidats (1 = top)
            meilleurs_rang = min(classement[i] for i in candidats)
            winners = [i for i in candidats if classement[i] == meilleurs_rang]

            # partage équitable
            part_entiere = pot // len(winners)
            reste = pot - part_entiere * len(winners)

            for i in winners:
                gains[joueurs[i]] += part_entiere

            # distribuer le reste suivant une règle déterministe :
            # par ex. au winner ayant l'indice minimal dans la table (ou selon dealer).
            # Ici on donne le reste aux winners dans l'ordre d'apparition.
            for k in range(reste):
                gains[joueurs[winners[k % len(winners)]]] += 1

        return gains

    @log
    def action(self, id_joueur: int, action: str, credit_joueur: int = 0, relance: int = 0) -> dict:
        """
        Effectue l'action souhaitée d'un joueur et met à jour la manche

        Paramètres
        ----------
        joueur : Joueur
            Le joueur effectuant l'action
        action : str
            Action souhaitée ("checker", "suivre", "all-in", "se coucher")
        relance : int, optionnel
            Montant de la relance si action = "suivre"

        Renvois
        -------
        int ou dict[joueur, int]
            Montant misé si tour non terminé
            gains si fin de manche

        Exceptions
        ----------
        Exception
            si ce n'est pas au joueur de jouer ou si la manche est terminée
        ValueError
            si l'action est invalide
        """

        indice_joueur = self.indice_joueur(id_joueur)

        if indice_joueur != self.indice_joueur_actuel:
            raise Exception(f"Ce n'est pas à vous de jouer !")
        if self.fin:
            raise Exception("La manche est déjà terminée, aucune action ne peut être effectuée")

        if action == "checker":
            montant = self.checker(indice_joueur)
        elif action == "suivre":
            montant = self.suivre(indice_joueur, credit_joueur, relance)
        elif action == "all-in":
            montant = self.all_in(indice_joueur, credit_joueur)
        elif action == "se coucher":
            montant = self.se_coucher(indice_joueur)
        else:
            actions = ("checker", "suivre", "all-in", "se coucher")
            raise ValueError(f"L'action {action} n'existe pas, actions possibles {actions}")

        if self.fin_de_manche():
            # On passe les tours jusqu'au dernier en cas de fin de manche avant le dernier tour
            if self.tour == 0:
                for _ in range(3):
                    self.__reserve.bruler()
                    self.__reserve.reveler(self.__board)
            if self.tour <= 1:
                self.__reserve.bruler()
                self.__reserve.reveler(self.__board)
            if self.tour <= 2:
                self.__reserve.bruler()
                self.__reserve.reveler(self.__board)

            self.__fin = True
            return montant

        if self.fin_du_tour():
            if self.tour == 0:
                self.flop()
            elif self.tour == 1:
                self.turn()
            elif self.tour == 2:
                self.river()
            return montant

        self.joueur_suivant()
        return montant

    def terminer_manche(self) -> dict:
        """Termine la manche et retourne les gains de chaque joueurs"""
        if self.__enregistree:
            return

        if not self.fin:
            raise Exception("La manche n'est pas encore terminée !")
        else:
            gains = self.gains()
            self.__enregistree = True
            return gains

    def resultats(self) -> str:
        """Affiche le détail complet de fin de partie"""

        texte = "Combinaisons :\n"

        if len(self.joueurs_en_lice) > 1:
            for j in range(len(self.info.joueurs)):
                if j in self.joueurs_en_lice:
                    combinaison = EvaluateurCombinaison().eval(
                        self.board.cartes + self.info.mains[j].cartes
                    )
                    texte += f"{self.info.pseudos[j]} : {combinaison}\n"
                else:
                    texte += f"{self.info.pseudos[j]} : [?]\n"

        else:
            texte += "NA : seul un joueur ne s'est pas couché"

        texte += "\nGains :\n"

        if len(self.joueurs_en_lice) > 1:
            for j in range(len(self.info.joueurs)):
                id_joueur = self.info.joueurs[j]
                gain = self.gains()[id_joueur]
                texte += f"{self.info.pseudos[j]} : {gain}\n"
        else:
            gain = self.valeur_pot()
            texte += f"{self.info.pseudos[self.joueurs_en_lice[0]]} : {gain}"

        return texte
