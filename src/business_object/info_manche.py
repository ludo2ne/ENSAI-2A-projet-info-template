"""Implémentation de la classe InfoManche"""

from business_object.main import Main


class InfoManche:
    """Contient toutes les informations relatives à une manche de poker"""

    __STATUTS = ("innactif", "en retard", "à jour", "couché", "all in")

    def __init__(self, joueurs: list[int], pseudos: list[str] = None):
        """
        Crée une nouvelle instance d'InfoManche pour suivre une manche.

        Paramètres
        ----------
        joueurs : list[Joueur]
            Liste des joueurs participant à la manche.

        Exceptions
        ----------
        TypeError
            Si `joueurs` n'est pas une liste de Joueur.
        ValueError
            Si la liste contient moins de deux joueurs.
        """

        if not isinstance(joueurs, list):
            raise TypeError(
                f"Le paramètre 'joueurs' doit être une liste, pas {type(joueurs).__name__}"
            )

        if not all(isinstance(j, int) for j in joueurs):
            raise TypeError("Tous les éléments de 'joueurs' doivent être des int")

        if len(joueurs) < 2:
            raise ValueError(
                f"Au moins deux joueurs doivent être présents : {len(joueurs)} présents"
            )

        self.__joueurs = joueurs
        self.__pseudos = pseudos
        self.__statuts = [0 for _ in joueurs]
        self.__mains = [None for _ in joueurs]
        self.__mises = [0 for _ in joueurs]
        self.__tour_couche = [None for _ in joueurs]

    @property
    def joueurs(self) -> list[int]:
        """
        Renvoie la liste des joueurs participant à la manche.

        Renvois
        -------
        list[Joueur]
            Les joueurs actifs de la manche.
        """

        return self.__joueurs

    @property
    def pseudos(self) -> list[str]:
        """Renvoie le pseudo des joueurs"""
        return self.__pseudos

    @property
    def statuts(self) -> list[int]:
        """
        Renvoie la liste des statuts des joueurs.

        Chaque statut est représenté par un entier selon la liste interne __STATUTS.

        Renvois
        -------
        list[int]
            Statuts des joueurs.
        """

        return self.__statuts

    @property
    def mains(self) -> list[Main]:
        """
        Renvoie la liste des mains assignées aux joueurs.

        Renvois
        -------
        list[Main]
            Les mains de chaque joueur.
        """

        return self.__mains

    @property
    def mises(self) -> list[int]:
        """
        Renvoie les mises actuelles de chaque joueur.

        Renvois
        -------
        list[int]
            Montants misés par les joueurs.
        """

        return self.__mises

    @property
    def tour_couche(self) -> list[int]:
        """
        Indique si un joueur est couché lors d'un tour.

        Renvois
        -------
        list[int | None]
            None pour un joueur actif, sinon le numéro du tour où il s'est couché.
        """

        return self.__tour_couche

    def __str__(self) -> str:
        """
        Représentation informelle de l'objet pour l'affichage.

        Paramètres
        ----------
        None

        Renvois
        -------
        str
            Description rapide de l'état de la manche.
        """

        return (
            f"InfoManche(joueurs={self.joueurs}, "
            f"statuts={self.statuts}, "
            f"mains={self.mains}, "
            f"mises={self.mises}, "
            f"tour_couche={self.tour_couche})"
        )

    def affichage_tout_joueur(self) -> str:
        pseudos = [p for p in self.pseudos]
        statuts = [self.__STATUTS[s] for s in self.__statuts]
        mises = [str(m) for m in self.__mises]
        couches = [str(t) if t is not None else "-" for t in self.__tour_couche]

        col_widths = [
            max(len(pseudo), len(statut), len(mise), len(couche), 7)
            for pseudo, statut, mise, couche in zip(pseudos, statuts, mises, couches)
        ]

        def row(label, values):
            """Construit une ligne du tableau, en centrant les valeurs."""
            cells = [f"{v:^{col_widths[i]}}" for i, v in enumerate(values)]
            return f"{label:<12} | " + " | ".join(cells) + " |"

        lines = []
        separator = "-" * (14 + sum(col_widths) + 3 * len(col_widths))

        lines.append(separator)
        lines.append(row("Joueurs", pseudos))
        lines.append(separator)
        lines.append(row("Statuts", statuts))
        lines.append(row("Mises", mises))
        lines.append(row("Couché au", couches))
        lines.append(separator)

        return "\n".join(lines)

    def modifier_statut(self, indice_joueur, statut: int) -> None:
        """
        Modifie le statut d'un joueur.

        Paramètres
        ----------
        indice_joueur : int
            Indice du joueur dans la liste.
        statut : int
            Nouveau statut du joueur.

        Renvois
        -------
        None
        """

        self.__statuts[indice_joueur] = statut

    def modifier_mise(self, indice_joueur, nouveau_montant: int) -> None:
        """
        Met à jour la mise d'un joueur pour le tour courant.

        Paramètres
        ----------
        indice_joueur : int
            Indice du joueur dans la liste.
        nouveau_montant : int
            Nouveau montant de la mise.

        Renvois
        -------
        None
        """
        self.__mises[indice_joueur] = nouveau_montant

    def modifier_tour_couche(self, indice_joueur, tour: int) -> None:
        """
        Enregistre le tour auquel un joueur s'est couché.

        Paramètres
        ----------
        indice_joueur : int
            Indice du joueur dans la liste.
        tour : int
            Numéro du tour où le joueur s'est couché.

        Renvois
        -------
        None
        """

        self.__tour_couche[indice_joueur] = tour

    def assignation_mains(self, mains: list[Main]) -> None:
        """
        Assigne les mains distribuées aux joueurs.

        Paramètres
        ----------
        mains : list[Main]
            Liste des mains distribuées correspondant à chaque joueur.

        Renvois
        -------
        None

        Exceptions
        ----------
        TypeError
            si `mains` n'est pas une liste de Main.
        ValueError
            si le nombre de mains ne correspond pas au nombre de joueurs.
        """

        if not isinstance(mains, list) or not all(isinstance(m, Main) for m in mains):
            raise TypeError("Le paramètre 'mains' doit être une liste de Main")

        if len(mains) != len(self.joueurs):
            raise ValueError("Le nombre de mains doit correspondre au nombre de joueurs")

        self.__mains = mains
