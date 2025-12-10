import pytest
from business_object.combinaison.couleur import Couleur
from business_object.combinaison.quinte import Quinte
from business_object.combinaison.quinte_flush import QuinteFlush
from business_object.combinaison.brelan import Brelan
from business_object.combinaison.double_paire import DoublePaire
from business_object.combinaison.carre import Carre
from business_object.combinaison.full import Full
from business_object.combinaison.paire import Paire
from business_object.combinaison.simple import Simple
from business_object.evaluateur_combinaison import EvaluateurCombinaison


def get_kicker_valeurs(kicker):
    """Retourne toujours une liste de valeurs de cartes même si kicker est string ou tuple/list"""
    if kicker is None:
        return []
    if isinstance(kicker, (list, tuple)):
        return list(kicker)
    return [kicker]


def test_eval_full():
    # GIVEN: une liste de cartes formant un Full
    cartes = [
        pytest.roi_coeur,
        pytest.roi_pique,
        pytest.roi_carreau,
        pytest.dame_trefle,
        pytest.dame_coeur,
    ]

    # WHEN: on évalue la combinaison
    combi = EvaluateurCombinaison.eval(cartes)

    # THEN
    assert isinstance(combi, Full)
    assert combi.hauteur == ["Roi", "Dame"]
    assert combi.kicker is None


def test_eval_paire():
    # GIVEN: une liste de cartes formant une Paire
    cartes = [
        pytest.roi_coeur,
        pytest.roi_pique,
        pytest.dame_carreau,
        pytest.dix_trefle,
        pytest.neuf_coeur,
    ]

    # WHEN: on évalue la combinaison
    combi = EvaluateurCombinaison.eval(cartes)

    # THEN:
    assert isinstance(combi, Paire)
    assert combi.hauteur == "Roi"
    assert get_kicker_valeurs(combi.kicker) == ["Dame", "10", "9"]


def test_eval_simple():
    # GIVEN:
    cartes = [
        pytest.as_coeur,
        pytest.roi_pique,
        pytest.dame_carreau,
        pytest.dix_trefle,
        pytest.neuf_coeur,
    ]

    # WHEN: on évalue la combinaison
    combi = EvaluateurCombinaison.eval(cartes)

    # THEN
    assert isinstance(combi, Simple)
    assert combi.hauteur == "As"
    assert get_kicker_valeurs(combi.kicker) == ["Roi", "Dame", "10", "9"]

def test_eval_couleur():
    cartes = [
        pytest.as_coeur,
        pytest.roi_coeur,
        pytest.dame_coeur,
        pytest.dix_coeur,
        pytest.deux_coeur,
    ]
    combi = EvaluateurCombinaison.eval(cartes)
    assert isinstance(combi, Couleur)

def test_eval_quinte():
    cartes = [
        pytest.cinq_coeur,
        pytest.six_pique,
        pytest.sept_carreau,
        pytest.huit_trefle,
        pytest.neuf_coeur,
    ]
    combi = EvaluateurCombinaison.eval(cartes)
    assert isinstance(combi, Quinte)

def test_eval_quinte_flush():
    cartes = [
        pytest.cinq_coeur,
        pytest.six_coeur,
        pytest.sept_coeur,
        pytest.huit_coeur,
        pytest.neuf_coeur,
    ]
    combi = EvaluateurCombinaison.eval(cartes)
    assert isinstance(combi, QuinteFlush)

def test_eval_brelan():
    cartes = [
        pytest.roi_coeur,
        pytest.roi_pique,
        pytest.roi_trefle,
        pytest.dame_carreau,
        pytest.dix_trefle,
    ]
    combi = EvaluateurCombinaison.eval(cartes)
    assert isinstance(combi, Brelan)

def test_eval_double_paire():
    cartes = [
        pytest.roi_coeur,
        pytest.roi_pique,
        pytest.dame_coeur,
        pytest.dame_pique,
        pytest.neuf_carreau,
    ]
    combi = EvaluateurCombinaison.eval(cartes)
    assert isinstance(combi, DoublePaire)

def test_eval_carre():
    cartes = [
        pytest.roi_coeur,
        pytest.roi_pique,
        pytest.roi_carreau,
        pytest.roi_trefle,
        pytest.dame_coeur,
    ]
    combi = EvaluateurCombinaison.eval(cartes)
    assert isinstance(combi, Carre)

def test_eval_erreur_moins_de_5_cartes():
    with pytest.raises(ValueError):
        EvaluateurCombinaison.eval([])

    with pytest.raises(ValueError):
        EvaluateurCombinaison.eval([pytest.as_coeur, pytest.roi_pique])

def test_eval_aucune_combinaison_retourne_simple():
    cartes = [
        pytest.as_coeur,     # As
        pytest.roi_pique,    # Roi
        pytest.huit_trefle,  # 8
        pytest.six_carreau,  # 6
        pytest.trois_coeur   # 3
    ]

    combi = EvaluateurCombinaison.eval(cartes)

    assert isinstance(combi, Simple)
