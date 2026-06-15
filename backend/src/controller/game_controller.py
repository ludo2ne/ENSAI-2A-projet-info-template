from fastapi import APIRouter, Depends

from schema.game_model import GamePlayModel
from service.game_service import GameService
from utils.security import verify_token

router = APIRouter()


def get_game_service():
    """Dependency provider for GameService."""
    return GameService()


@router.post("/", tags=["Games"], response_model=dict)
def play_game(
    req: GamePlayModel, game_service=Depends(get_game_service), current_player=Depends(verify_token)
):
    """Starts and executes a new game session.
    Args:
        req (GamePlayModel): Request containing player IDs and game mode.
        game_service (GameService): Service handling game logic.
        current_player (Player): The authenticated user.
    Returns:
        dict: Match summary including player usernames, result, winner,
            and updated ELO ratings.
    Raises:
        HTTPException: 401 if unauthenticated, 400 if invalid request.
    """
    return game_service.play(current_player.id_player, req.id_opponent, req.choice)
