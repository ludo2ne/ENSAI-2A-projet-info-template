from fastapi import APIRouter
from pydantic import BaseModel

from service.game_service import GameService

router = APIRouter()
game_service = GameService()


class GameRequest(BaseModel):
    player1_id: int
    player2_id: int
    choice: str


@router.post("/", tags=["Games"])
def play_game(req: GameRequest):
    return game_service.play(req.player1_id, req.player2_id, req.choice)
