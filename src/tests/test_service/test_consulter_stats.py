import pytest
from unittest.mock import patch, MagicMock
from service.consulter_stats import ConsulterStats

# Création d'une instance de la classe ConsulterStats
consulter_stats = ConsulterStats()


@pytest.mark.parametrize(
    "equipe_nom, region, goals, goals_par_match, assists, assists_par_match, shots, shots_par_match, saves, saves_par_match, score, score_par_match, shooting_percentage, demo_inflige, demo_inflige_par_match, time_offensive_third, indice_offensif, indice_performance",
    [("RocketLag", "EU", 5, 2.5, 3, 1.5, 12, 6, 4, 2, 1500, 750, 40, 3, 1.5, 600, 11.38, 4.93)],
)
@patch("dao.joueur_dao.JoueurDao")
@patch("dao.match_dao.MatchDao")
def test_stats_joueurs_nom_valide(
    MockMatchDao,
    MockJoueurDao,
    equipe_nom,
    region,
    goals,
    goals_par_match,
    assists,
    assists_par_match,
    shots,
    shots_par_match,
    saves,
    saves_par_match,
    score,
    score_par_match,
    shooting_percentage,
    demo_inflige,
    demo_inflige_par_match,
    time_offensive_third,
    indice_offensif,
    indice_performance,
):
    # Nom du joueur à tester
    nom_joueur = "Crispy"

    # Simule un joueur avec des statistiques fictives
    joueur_fictif = MagicMock(
        region=region,
        equipe=equipe_nom,
        goals=goals,
        assists=assists,
        shots=shots,
        saves=saves,
        score=score,
        shooting_percentage=shooting_percentage,
        demo_inflige=demo_inflige,
        time_offensive_third=time_offensive_third,
    )

    # Mock des méthodes de DAO pour obtenir les statistiques
    MockJoueurDao.return_value.obtenir_par_nom.return_value = joueur_fictif
    MockMatchDao.return_value.trouver_id_match_par_joueur.return_value = [1, 2]

    # Appel de la méthode à tester
    stats_result = consulter_stats.stats_joueurs(nom_joueur)

    # Vérifier que le joueur a bien été récupéré par son nom
    MockJoueurDao.return_value.obtenir_par_nom.assert_called_once_with(nom_joueur)
    MockMatchDao.return_value.trouver_id_match_par_joueur.assert_called_once_with(nom_joueur)

    # Assertions pour vérifier les statistiques retournées
    assert stats_result.nom == nom_joueur
    assert stats_result.equipe_nom == equipe_nom
    assert stats_result.goals == goals
    assert stats_result.goals_par_match == goals_par_match
    assert stats_result.assists == assists
    assert stats_result.assists_par_match == assists_par_match
    assert stats_result.shots == shots
    assert stats_result.shots_par_match == shots_par_match
    assert stats_result.saves == saves
    assert stats_result.saves_par_match == saves_par_match
    assert stats_result.score == score
    assert stats_result.score_par_match == score_par_match
    assert stats_result.shooting_percentage == shooting_percentage
    assert stats_result.demo_inflige == demo_inflige
    assert stats_result.demo_inflige_par_match == demo_inflige_par_match
    assert stats_result.time_offensive_third == time_offensive_third
    assert round(stats_result.indice_offensif, 2) == indice_offensif
    assert round(stats_result.indice_performance, 2) == indice_performance
