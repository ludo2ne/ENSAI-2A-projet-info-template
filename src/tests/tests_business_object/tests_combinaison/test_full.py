import pytest

from business_object.combinaison.full import Full


def test_force_full():
    # GIVEN: Classe Full
    # WHEN / THEN
    assert Full.FORCE() == 6


@pytest.mark.parametrize(
    "cartes,expected",
    [
        # Full présent
        (
            [
                pytest.dame_coeur,
                pytest.dame_pique,
                pytest.dame_trefle,
                pytest.roi_coeur,
                pytest.roi_carreau,
            ],
            True,
        ),
        ([pytest.dame_coeur, pytest.dame_pique, pytest.roi_coeur, pytest.roi_carreau], False),
        (
            [
                pytest.dame_coeur,
                pytest.dame_pique,
                pytest.dame_trefle,
                pytest.dame_carreau,
                pytest.roi_coeur,
            ],
            False,
        ),
    ],
)
def test_est_present_full(cartes, expected):
    # GIVEN: Une liste de cartes
    # WHEN: On teste la présence d'un Full
    result = Full.est_present(cartes)
    # THEN
    assert result is expected


def test_from_cartes_valide_full():
    # GIVEN:
    cartes = [
        pytest.dame_coeur,
        pytest.dame_pique,
        pytest.dame_trefle,
        pytest.roi_coeur,
        pytest.roi_carreau,
        pytest.as_coeur,
        pytest.valet_coeur,
    ]
    # WHEN
    full = Full.from_cartes(cartes)
    # THEN
    assert full.hauteur == ["Dame", "Roi"]
    assert full.kicker is None


def test_from_cartes_invalide_full():
    # GIVEN: cartes ne formant pas un Full
    cartes = [
        pytest.dame_coeur,
        pytest.dame_pique,
        pytest.valet_coeur,
        pytest.roi_coeur,
        pytest.as_coeur,
    ]
    # WHEN / THEN: doit lever ValueError
    with pytest.raises(ValueError):
        Full.from_cartes(cartes)


def test_comparaison_full():
    # GIVEN: Deux Full différents
    cartes_1 = [
        pytest.dame_coeur,
        pytest.dame_pique,
        pytest.dame_trefle,
        pytest.roi_coeur,
        pytest.roi_carreau,
    ]
    cartes_2 = [
        pytest.valet_coeur,
        pytest.valet_pique,
        pytest.valet_trefle,
        pytest.as_coeur,
        pytest.as_pique,
    ]
    full1 = Full.from_cartes(cartes_1)
    full2 = Full.from_cartes(cartes_2)
    # THEN
    assert full1 > full2
    assert full2 < full1
    assert full1 == Full.from_cartes(cartes_1)


def test_str_repr_full():
    # GIVEN
    cartes = [
        pytest.dame_coeur,
        pytest.dame_pique,
        pytest.dame_trefle,
        pytest.roi_coeur,
        pytest.roi_carreau,
    ]
    full = Full.from_cartes(cartes)
    # THEN
    assert str(full) == "Full Dame Roi"
    assert repr(full) == "Full(hauteur=['Dame', 'Roi'], kicker=None)"

def test_from_cartes_brelan_sans_paire():
    # GIVEN : un brelan mais aucune paire distincte
    cartes = [
        pytest.dame_coeur,
        pytest.dame_pique,
        pytest.dame_trefle,  # brelan
        pytest.roi_coeur,
        pytest.as_coeur,
    ]

    # WHEN / THEN : on doit lever l'erreur spécifique de manque de paire
    with pytest.raises(ValueError, match="Aucune paire pour former un Full"):
        Full.from_cartes(cartes)
