from fastapi import APIRouter

from schema.game_model import GameModel
from service.game_service import GameService

router = APIRouter()
game_service = GameService()


@router.post("/", tags=["Games"])
def play_game(req: GameModel):
    return game_service.play(req.player1_id, req.player2_id, req.choice)
