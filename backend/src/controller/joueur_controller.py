# controller/joueur_controller.py

import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from service.joueur_service import JoueurService

router = APIRouter()
joueur_service = JoueurService()


class JoueurModel(BaseModel):
    """Définir un modèle Pydantic pour les Joueurs"""

    id_joueur: int | None = None
    pseudo: str
    mdp: str
    age: int
    mail: str
    fan_pokemon: bool


@router.get("/", tags=["Joueurs"])
async def lister_tous_joueurs():
    """Lister tous les joueurs"""
    logging.info("Lister tous les joueurs")
    liste_joueurs = joueur_service.lister_tous()
    return liste_joueurs


@router.get("/{id_joueur}", tags=["Joueurs"])
async def joueur_par_id(id_joueur: int):
    """Trouver un joueur à partir de son id"""
    logging.info("Trouver un joueur à partir de son id")
    joueur = joueur_service.trouver_par_id(id_joueur)
    if not joueur:
        raise HTTPException(status_code=404, detail="Joueur non trouvé")
    return joueur


@router.post("/", tags=["Joueurs"])
async def creer_joueur(j: JoueurModel):
    """Créer un joueur"""
    logging.info("Créer un joueur")
    if joueur_service.pseudo_deja_utilise(j.pseudo):
        raise HTTPException(status_code=400, detail="Pseudo déjà utilisé")

    joueur = joueur_service.creer(j.pseudo, j.mdp, j.age, j.mail, j.fan_pokemon)
    if not joueur:
        raise HTTPException(status_code=500, detail="Erreur lors de la création du joueur")

    return joueur


@router.put("/{id_joueur}", tags=["Joueurs"])
async def modifier_joueur(id_joueur: int, j: JoueurModel):
    """Modifier un joueur"""
    logging.info("Modifier un joueur")
    joueur = joueur_service.trouver_par_id(id_joueur)
    if not joueur:
        raise HTTPException(status_code=404, detail="Joueur non trouvé")

    joueur.pseudo = j.pseudo
    joueur.mdp = j.mdp
    joueur.age = j.age
    joueur.mail = j.mail
    joueur.fan_pokemon = j.fan_pokemon

    joueur = joueur_service.modifier(joueur)
    if not joueur:
        raise HTTPException(status_code=500, detail="Erreur lors de la modification du joueur")

    return f"Joueur {j.pseudo} modifié"


@router.delete("/{id_joueur}", tags=["Joueurs"])
async def supprimer_joueur(id_joueur: int):
    """Supprimer un joueur"""
    logging.info("Supprimer un joueur")
    joueur = joueur_service.trouver_par_id(id_joueur)
    if not joueur:
        raise HTTPException(status_code=404, detail="Joueur non trouvé")

    joueur_service.supprimer(joueur)
    return f"Joueur {joueur.pseudo} supprimé"
