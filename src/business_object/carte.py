"""Implémentation de la classe Carte"""


class Carte:
    """Modélisation d'une carte dans un jeu de cartes"""

    """Attributs de la classe"""
    __VALEURS = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "Valet", "Dame", "Roi", "As")
    __COULEURS = ("Pique", "Carreau", "Coeur", "Trêfle")

    def __init__(self, valeur: str, couleur: str) -> "Carte":
        """
        Instanciation d'une carte (Jeu de cartes)

        Paramètres
        ----------
        valeur : str
            Valeur de la carte (de l'"as" jusqu'au "roi")
        couleur : str
            Couleur de la carte parmi "Pique", "Carreau", "Coeur" et "Trêfle"

        Renvois
        -------
        Carte
            Instance de 'Carte'

        Exceptions
        ----------
        ValueError
            si la valeur n'existe pas dans un jeu de cartes
            si la couleur n'existe pas dans un jeu de cartes
        """

        if valeur not in self.__VALEURS:
            raise ValueError(f"Valeur de la carte incorrecte : {valeur}")
        if couleur not in self.__COULEURS:
            raise ValueError(f"Couleur de la carte incorrecte : {couleur}")

        self.__valeur = valeur
        self.__couleur = couleur

    @classmethod
    def VALEURS(cls) -> tuple[str]:
        """Retourne la liste des valeurs possibles d'une carte"""
        return cls.__VALEURS

    @classmethod
    def COULEURS(cls) -> tuple:
        """Retourne la liste des couleurs possibles d'une carte"""
        return cls.__COULEURS

    @property
    def valeur(self) -> str:
        """Retourne la valeur de la carte"""
        return self.__valeur

    @property
    def couleur(self) -> str:
        """Retourne la couleur de la carte"""
        return self.__couleur

    def __str__(self) -> str:
        """Représentation informelle d'un objet de type Carte"""
        return f"{self.__valeur} de {self.__couleur.lower()}"

    def __repr__(self) -> str:
        """Représentation formelle d'un objet de type Carte"""
        return f"Carte({self.__valeur}, {self.__couleur})"

    def __eq__(self, other) -> bool:
        """
        Egalité entre deux Cartes

        Paramètres
        ----------
        other : any
            objet comparée

        Renvois
        -------
        bool
            Vrai si la valeur et la couleur des deux cartes comparées sont identiques
        """

        if not isinstance(other, Carte):
            return False

        return self.__valeur == other.__valeur and self.__couleur == other.__couleur

    def __lt__(self, other) -> bool:
        """
        Vérifie si la valeur de la carte est plus petite que celle de l'autre carte

        Paramètres
        ----------
        other : Carte
            carte comparée

        Renvois
        -------
        bool
            Vrai si la valeur de la carte est plus faible que la seconde
        """

        if not isinstance(other, Carte):
            raise TypeError(f"L'objet comparé n'est pas de type Carte : {type(other)}")

        return self.VALEURS().index(self.valeur) < self.VALEURS().index(other.valeur)

    def __gt__(self, other) -> bool:
        """
        Vérifie si la valeur de la carte est plus grande que celle de l'autre carte

        Paramètres
        ----------
        other : Carte
            carte comparée

        Renvois
        -------
        bool
            Vrai si la valeur de la carte est plus forte que la seconde
        """

        if not isinstance(other, Carte):
            raise TypeError(f"L'objet comparé n'est pas de type Carte : {type(other)}")

        return self.VALEURS().index(self.valeur) > self.VALEURS().index(other.valeur)

    def __hash__(self) -> int:
        """Code de hachage déterminé selon la représentation officielle de la carte"""
        return hash(self.__repr__())

    def valeur_egale(self, other) -> bool:
        """
        Vérifie l'égalité de valeurs entre deux Cartes

        Paramètres
        ----------
        other : Carte
            carte comparée

        Renvois
        -------
        bool
            Vrai si la valeur des deux cartes comparées sont identiques

        """

        if not isinstance(other, Carte):
            raise TypeError(f"L'objet comparé n'est pas de type Carte : {type(other)}")

        return self.VALEURS().index(self.valeur) == self.VALEURS().index(other.valeur)
