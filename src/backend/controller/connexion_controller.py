from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from service.joueur_service import JoueurService

router = APIRouter()
service = JoueurService()


class ConnexionRequest(BaseModel):
    pseudo: str
    mdp: str


@router.post("/", tags=["Connexion"])
def connexion(req: ConnexionRequest):
    joueur = service.se_connecter(req.pseudo, req.mdp)
    if joueur:
        return {"id": joueur.id, "pseudo": joueur.pseudo}
    raise HTTPException(status_code=401, detail="Identifiants invalides")
