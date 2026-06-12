from fastapi import APIRouter, Depends

from schema.game_model import GameModel
from service.game_service import GameService

router = APIRouter()


def get_game_service():
    """Dependency provider for GameService."""
    return GameService()


@router.post("/", tags=["Games"])
def play_game(req: GameModel, game_service=Depends(get_game_service)):
    """Executes a game session.
    Args:
        req (GameModel): Request containing player IDs and game choice.
    Returns:
        dict: Match results (winner, result, new elo, etc.)."""
    return game_service.play(req.id_player1, req.id_player2, req.choice)
