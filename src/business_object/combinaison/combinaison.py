from abc import ABC, abstractmethod
from functools import total_ordering
from typing import List, Optional, Tuple, Union

from business_object.carte import Carte


@total_ordering
class AbstractCombinaison(ABC):
    """
    Initialise une combinaison de cartes avec sa hauteur et ses kickers.

    Paramètres
    ----------
    hauteur : str | list[str] | tuple[str, ...]
        Carte(s) principale(s) définissant la combinaison.
    kicker : str | list[str] | tuple[str, ...] | None, optionnel
        Carte(s) servant à départager des combinaisons de même hauteur.

    Exceptions
    ----------
    TypeError
        Levée si les types de `hauteur` ou `kicker` ne sont pas valides.
    """

    def __init__(
        self,
        hauteur: Union[str, Tuple[str, ...], List[str]],
        kicker: Optional[Union[str, Tuple[str, ...], List[str]]] = None,
    ) -> None:
        # Normalisation de la hauteur
        if isinstance(hauteur, (list, tuple)):
            hauteur = hauteur[0] if len(hauteur) == 1 else list(hauteur)
        elif not isinstance(hauteur, str):
            raise TypeError("La hauteur doit être un str, une liste ou un tuple.")

        # Normalisation du kicker
        if kicker is None:
            self._kicker = ()
        elif isinstance(kicker, str):
            self._kicker = (kicker,)
        elif isinstance(kicker, (list, tuple)):
            self._kicker = tuple(kicker)
        else:
            raise TypeError("Le kicker doit être un str, une liste, un tuple ou None.")

        self._hauteur = hauteur

    @staticmethod
    def verifier_min_cartes(cartes: list, n: int = 5) -> None:
        """
        Vérifie que la liste de cartes contient au moins 5 cartes.

        Paramètres
        ----------
        cartes : list
            Liste de cartes à vérifier.
        n : int, optionnel
            Nombre minimum de cartes requis (par défaut 5).

        Exceptions
        ----------
        ValueError
            Levée si le nombre de cartes est inférieur à 5.
        """
        if len(cartes) < n:
            raise ValueError(f"Au moins {n} cartes sont nécessaires pour cette combinaison.")

    @property
    def hauteur(self) -> Union[str, List[str]]:
        """
        Retourne la ou les cartes principales de la combinaison.

        Renvois
        -------
        str | list[str]
            La carte principale ou la liste des cartes principales.
        """
        if isinstance(self._hauteur, (list, tuple)):
            return self._hauteur[0] if len(self._hauteur) == 1 else list(self._hauteur)
        return self._hauteur

    @property
    def kicker(self) -> Optional[Union[str, Tuple[str, ...]]]:
        """
        Retourne les kickers utilisés pour départager des combinaisons.

        Renvois
        -------
        str | tuple[str, ...] | None
            Carte(s) servant de kicker, ou None s'il n'y en a pas.
        """
        if not self._kicker:
            return None
        return self._kicker[0] if len(self._kicker) == 1 else self._kicker

    # --- Méthodes abstraites ---
    @classmethod
    @abstractmethod
    def FORCE(cls) -> int:
        """
        Renvoie la force numérique de la combinaison.

        Renvois
        -------
        int
            Valeur permettant de comparer deux combinaisons.
        """
        pass # pragma: no cover

    @classmethod
    @abstractmethod
    def est_present(cls, cartes: List[Carte]) -> bool:
        """
        Indique si la combinaison est présente dans une liste de cartes.

        Paramètres
        ----------
        cartes : list[Carte]
            Cartes à analyser.

        Renvois
        -------
        bool
            True si la combinaison est détectée, False sinon.
        """
        pass # pragma: no cover

    @classmethod
    @abstractmethod
    def from_cartes(cls, cartes: List[Carte]) -> "AbstractCombinaison":
        """
        Construit une instance de la combinaison à partir d’une liste de cartes.

        Paramètres
        ----------
        cartes : list[Carte]
            Cartes à partir desquelles construire la combinaison.

        Renvois
        -------
        AbstractCombinaison
            Objet représentant la combinaison détectée.
        """
        pass # pragma: no cover

    # --- Comparaison entre combinaisons ---
    def _valeur_comparaison(self) -> Tuple[int, Tuple[int, ...], Tuple[int, ...]]:
        """
        Renvoie les valeurs numériques permettant de comparer deux combinaisons.

        Renvois
        -------
        tuple
            Triplet (force, indices hauteur, indices kicker) pour comparaison.
        """
        # Hauteur → indices
        if isinstance(self._hauteur, (list, tuple)):
            hauteur_vals = tuple(Carte.VALEURS().index(h) for h in self._hauteur)
        else:
            hauteur_vals = (Carte.VALEURS().index(self._hauteur),)

        # Kicker → indices
        if not self._kicker:
            kicker_vals = ()
        else:
            kicker_vals = tuple(Carte.VALEURS().index(k) for k in self._kicker)

        return (self.FORCE(), hauteur_vals, kicker_vals)

    def __eq__(self, other) -> bool:
        if not isinstance(other, AbstractCombinaison):
            return NotImplemented
        return self._valeur_comparaison() == other._valeur_comparaison()

    def __lt__(self, other) -> bool:
        if not isinstance(other, AbstractCombinaison):
            return NotImplemented
        return self._valeur_comparaison() < other._valeur_comparaison()

    # --- Représentations ---
    def _fmt_valeurs(self, val) -> Optional[str]:
        """
        Convertit un tuple ou une liste de valeurs en chaîne lisible.

        Paramètres
        ----------
        val : str | list | tuple | None
            Valeur(s) à formatter.

        Renvois
        -------
        str | None
            Chaîne représentant la/les valeurs, ou None si vide.
        """
        """Convertit un tuple ou une liste en chaîne lisible."""
        if val is None:
            return None
        if isinstance(val, (tuple, list)):
            return val[0] if len(val) == 1 else " et ".join(val)
        return val

    def __str__(self) -> str:
        """
        Représentation lisible de la combinaison pour affichage.

        Renvois
        -------
        str
            Chaîne décrivant la combinaison, ex : "Brelan de Roi".
        """
        h = self._fmt_valeurs(self.hauteur)
        nom = self.__class__.__name__
        return f"{nom} d'{h}" if h == "As" else f"{nom} de {h}"

    def __repr__(self) -> str:
        """
        Représentation technique de la combinaison pour debug.

        Renvois
        -------
        str
            Chaîne détaillant la hauteur et les kickers, ex : "Brelan(hauteur=Roi, kicker=As)".
        """
        h = self._fmt_valeurs(self.hauteur)
        k = self._fmt_valeurs(self.kicker)
        return (
            f"{self.__class__.__name__}(hauteur={h})"
            if not self._kicker
            else f"{self.__class__.__name__}(hauteur={h}, kicker={k})"
        )
