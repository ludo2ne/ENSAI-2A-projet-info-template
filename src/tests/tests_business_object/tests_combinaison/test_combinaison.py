import pytest

from business_object.combinaison.combinaison import AbstractCombinaison


class CombinaisonTest(AbstractCombinaison):
    @classmethod
    def FORCE(cls) -> int:
        return 1

    @classmethod
    def est_present(cls, cartes):
        return True

    @classmethod
    def from_cartes(cls, cartes):
        return cls("As")


@pytest.mark.parametrize(
    "hauteur,kicker,expected_hauteur,expected_kicker",
    [
        ("As", None, "As", None),
        (["Roi"], None, "Roi", None),
        (("Dame",), None, "Dame", None),
        (["10", "9"], ["8"], ["10", "9"], "8"),
        ("Valet", ["2", "3"], "Valet", ("2", "3")),
        ("As", "Roi", "As", "Roi"),
        (["7"], ("6",), "7", "6"),
        (("5", "4"), ("3", "2"), ["5", "4"], ("3", "2")),
    ],
)
def test_combinaison_init(hauteur, kicker, expected_hauteur, expected_kicker):
    # GIVEN: Une hauteur et un kicker
    c = CombinaisonTest(hauteur, kicker)

    # WHEN: On accède aux propriétés
    h = c.hauteur
    k = c.kicker

    # THEN: Les propriétés doivent correspondre aux valeurs normalisées
    assert h == expected_hauteur
    assert k == expected_kicker


@pytest.mark.parametrize(
    "hauteur,kicker",
    [
        ("As", None),
        ("Roi", "Dame"),
        (["10", "9"], ["8"]),
        (("5", "4"), ("3", "2")),
    ],
)
def test_combinaison_valeur_comparaison(hauteur, kicker):
    # GIVEN: Une combinaison avec hauteur et kicker
    c = CombinaisonTest(hauteur, kicker)

    # WHEN: On calcule la valeur de comparaison
    force, hauteur_vals, kicker_vals = c._valeur_comparaison()

    # THEN
    assert isinstance(force, int)
    assert all(isinstance(v, int) for v in hauteur_vals)
    assert all(isinstance(k, int) for k in kicker_vals)


def test_combinaison_comparaison():
    # GIVEN: Plusieurs combinaisons
    c1 = CombinaisonTest("As", "Roi")
    c2 = CombinaisonTest("As", "Dame")
    c3 = CombinaisonTest("As", "Roi")
    c4 = CombinaisonTest("Roi", None)

    # WHEN / THEN:
    assert c1 > c2
    assert c2 < c1
    assert c1 == c3
    assert c1 != c2
    assert c2 != c4


@pytest.mark.parametrize(
    "hauteur,kicker",
    [
        ("As", None),
        ("Roi", "Dame"),
        (["10", "9"], ["8"]),
    ],
)
def test_combinaison_repr_str(hauteur, kicker):
    # GIVEN
    c = CombinaisonTest(hauteur, kicker)

    # WHEN
    s = str(c)
    r = repr(c)

    # THEN
    if isinstance(hauteur, (list, tuple)) and len(hauteur) > 1:
        for h in hauteur:
            assert h in s or " et " in s
    else:
        if hauteur == "As":
            assert "d'As" in s
        else:
            assert hauteur in s

    if kicker is not None:
        if isinstance(kicker, (list, tuple)):
            for k in kicker:
                assert k in r
        else:
            assert kicker in r
    else:
        assert "kicker" not in r


def test_combinaison_verifier_min_cartes():
    # GIVEN / WHEN
    CombinaisonTest.verifier_min_cartes([1, 2, 3, 4, 5])
    CombinaisonTest.verifier_min_cartes([1, 2, 3, 4, 5, 6], n=5)

    # THEN: Erreur si moins de 5 cartes
    with pytest.raises(ValueError):
        CombinaisonTest.verifier_min_cartes([1, 2, 3], n=5)

def test_combinaison_init_hauteur_invalide():
    with pytest.raises(TypeError):
        CombinaisonTest(123)  # hauteur invalide

def test_combinaison_init_kicker_invalide():
    with pytest.raises(TypeError):
        CombinaisonTest("As", kicker=123)

def test_combinaison_eq_autre_type():
    c = CombinaisonTest("As")
    other = 42  # objet d'un autre type

    # __eq__ doit renvoyer NotImplemented → Python interprète ça comme False
    assert (c == other) is False
    # Et l'opérateur inverse aussi
    assert (other == c) is False


def test_combinaison_lt_autre_type():
    c = CombinaisonTest("As")
    other = 42  # objet d'un autre type

    # __lt__ renvoie NotImplemented → Python doit lever TypeError
    with pytest.raises(TypeError):
        c < other
