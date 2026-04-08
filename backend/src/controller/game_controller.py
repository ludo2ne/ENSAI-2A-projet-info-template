from fastapi import APIRouter
from pydantic import BaseModel

from service.game_service import GameService

router = APIRouter()
game_service = GameService()


class PartieRequest(BaseModel):
    joueur1_id: int
    joueur2_id: int
    choice: str


@router.post("/", tags=["Games"])
def jouer_partie(req: PartieRequest):
    return game_service.play(req.joueur1_id, req.joueur2_id, req.choice)
