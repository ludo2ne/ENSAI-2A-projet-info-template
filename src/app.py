import logging
from typing import List

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel

from service.action_service import ActionService
from service.credit_service import CreditService
from service.joueur_service import JoueurService
from service.table_service import TableService
from utils.log_init import initialiser_logs
from utils.reset_database import ResetDatabase

app = FastAPI(title="ENS'ALL IN")


initialiser_logs("Webservice")

joueur_service = JoueurService()
credit_service = CreditService()
action_service = ActionService()
table_service = TableService()


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """Redirect to the API documentation"""
    return RedirectResponse(url="/docs")


class JoueurModel(BaseModel):
    """Définir un modèle Pydantic pour les Joueurs"""

    id_joueur: int | None = None  # Champ optionnel
    pseudo: str
    pays: str
    credit: int | None = None  # Champ optionnel


@app.put("/admin/crediter/{pseudo}/{montant}", tags=["Admin"])
async def crediter(pseudo: str, montant: int):
    joueur = joueur_service.trouver_par_pseudo(pseudo)
    credit_service.crediter(joueur, montant)
    message = f"L'admin a bien crédité {montant} à {joueur.pseudo}"
    return message


@app.put("/admin/debiter/{pseudo}/{montant}", tags=["Admin"])
async def debiter(pseudo, montant: int):
    joueur = joueur_service.trouver_par_pseudo(pseudo)
    credit_service.debiter(joueur.id_joueur, montant)
    message = f"l'admin a bien débité {montant} à {joueur.pseudo}"
    return message


@app.get("/joueur/", tags=["Joueurs"])
async def joueur_lister():
    """Liste tous les joueurs"""
    logging.info("Liste tous les joueurs")
    return joueur_service.lister_tous()


@app.get("/joueur/connexion/{pseudo}", tags=["Joueurs"])
async def joueur_connexion(pseudo: str):
    """Connecte le joueur"""
    logging.info("Connecte le joueur")

    try:
        return joueur_service.se_connecter(pseudo)

    except ValueError as e:
        # pseudo n'existe pas
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        # ex : joueur déjà connecté
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/joueur/deconnexion/{id_joueur}", tags=["Joueurs"])
async def joueur_deconnexion(id_joueur: int):
    """Deconnecte le joueur"""
    logging.info("Deconnecte le joueur")
    return joueur_service.deconnexion(id_joueur)


@app.get("/joueur/connectes/", tags=["Joueurs"])
async def joueur_connectes():
    """Liste tous les joueurs"""
    logging.info("Liste tous les joueurs connéctés")
    return joueur_service.joueurs_connectes()


@app.get("/joueur/connectes/id/{id_joueur}", tags=["Joueurs"])
async def joueur_par_id(id_joueur: int):
    """Trouver un joueur à partir de son id"""
    logging.info("Trouver un joueur à partir de son id")
    return joueur_service.trouver_par_id(id_joueur)


@app.post("/joueur/", tags=["Joueurs"])
async def creer_joueur(j: JoueurModel):
    """Créer un joueur"""
    logging.info("Créer un joueur")
    if joueur_service.pseudo_deja_utilise(j.pseudo):
        raise HTTPException(status_code=404, detail="Pseudo déjà utilisé")

    joueur = joueur_service.creer(j.pseudo, j.pays)
    if joueur is None:
        raise HTTPException(status_code=404, detail="Erreur lors de la création du joueur")

    return joueur


@app.put("/joueur/{id_joueur}/{pseudo}/{pays}", tags=["Joueurs"])
async def modifier_joueur(id_joueur: int, pseudo: str, pays: str):
    """Modifier un joueur"""
    logging.info("Modifier un joueur")
    joueur = joueur_service.trouver_par_id(id_joueur)
    if not joueur:
        raise HTTPException(status_code=404, detail="Joueur non trouvé")

    if not joueur_service.pseudo_deja_utilise(pseudo):
        joueur.changer_pseudo(pseudo)
    joueur.changer_pays(pays)
    joueur = joueur_service.modifier(joueur)
    if not joueur:
        raise HTTPException(status_code=404, detail="Erreur lors de la modification du joueur")

    return f"Joueur {pseudo} modifié"


@app.delete("/joueur/{pseudo}", tags=["Joueurs"])
async def supprimer_joueur(pseudo: str):
    """Supprimer un joueur"""
    logging.info("Supprimer un joueur")
    joueur = joueur_service.trouver_par_pseudo(pseudo)
    if not joueur:
        raise HTTPException(status_code=404, detail="Joueur non trouvé")

    joueur_service.supprimer(joueur)
    return f"Joueur {joueur.pseudo} supprimé"


class TableModel(BaseModel):
    """Définir un modèle Pydantic pour les Table"""

    numero_table: int | None = None  # Champ optionnel
    joueurs_max: int
    grosse_blind: int
    mode_jeu: int | None = None  # Champ optionnel
    joueurs: List[int] = []


@app.get("/table/", tags=["Table"])
async def liste_tables():
    """liste les tables"""
    logging.info("liste les tables")
    return table_service.affichages_tables()


@app.post("/table/", tags=["Table"])
async def creer_table(t: TableModel):
    """Créer une table"""
    logging.info("Créer une table")

    table = table_service.creer_table(t.joueurs_max, t.grosse_blind)
    return TableModel(
        numero_table=table.numero_table,
        joueurs_max=table.joueurs_max,
        grosse_blind=table.grosse_blind,
        mode_jeu=table.mode_jeu,
        joueurs=[],
    )


@app.get("/table/joueurs/{numero_table}", tags=["Table"])
async def joueurs_dans_table(numero_table: int):
    table = table_service.table_par_numero(numero_table)

    return table.id_joueurs


@app.put("/table/ajouter/{numero_table}/{id_joueur}", tags=["Table"])
async def ajouter_joueur(numero_table: int, id_joueur: int):
    """ajoute un joueur a la table"""
    logging.info(f"ajoute le joueur {id_joueur} a la table {numero_table}")
    joueur = joueur_service.trouver_par_id(id_joueur)
    table_service.ajouter_joueur(numero_table, id_joueur)
    return f"le joueur {joueur.pseudo} a été ajouté à la table {numero_table}"


@app.put("/table/retirer/{id_joueur}", tags=["Table"])
async def retirer_un_joueur(id_joueur: int):
    """retire un joueur a la table"""
    logging.info(f"retire le joueur {id_joueur} de la table")
    table_service.retirer_joueur(id_joueur)
    return "Vous avez quitté la table"


@app.delete("/table/{numero_table}", tags=["Table"])
async def supprimer_table(numero_table: int):
    """Supprimer une table"""
    logging.info("Supprimer une table")
    table_service.supprimer_table(numero_table)
    return f"Table {numero_table} supprimé"


@app.put("/manche/lancer/{numero_table}", tags=["Manche"])
async def lancer_manche(numero_table: int):
    logging.info("lance une manche")

    try:
        table_service.lancer_manche(numero_table)
        return {"message": f"Manche lancée sur la table {numero_table}"}

    except Exception as e:
        logging.error(f"Erreur lors du lancement de la manche : {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/manche/affichage/{numero_table}", tags=["Manche"])
async def affichage_general(numero_table: int):
    """affichage general"""
    logging.info("affichage general")
    return table_service.affichage_general(numero_table=numero_table)


@app.get("/manche/main/{numero_table}/{id_joueur}", tags=["Manche"])
async def regarder_main(id_joueur: int):
    """regarder sa main"""
    logging.info("regarder sa main")
    return table_service.regarder_main(id_joueur)


@app.put("/manche/terminer/{numero_table}", tags=["Manche"])
async def terminer_manche(numero_table: int):
    """termine une manche"""
    logging.info("termine une manche")
    texte = table_service.terminer_manche(numero_table=numero_table)
    return f"la manche est terminé sur la table {numero_table}\n\n" + texte


@app.get("/action/{id_joueur}", tags=["Action"])
async def manche_joueur(id_joueur: int):
    """Trouver la manche auquel joue le joueur"""
    logging.info("Trouver la manche auquel joue le joueur")
    return action_service.manche_joueur(id_joueur)


@app.put("/action/all_in/{id_joueur}", tags=["Action"])
async def all_in(id_joueur: int):
    """Joue all_in pour le joueur"""
    logging.info("Joue all_in pour le joueur")
    try:
        action_service.all_in(id_joueur)
        return {"success": True, "message": f"Joueur {id_joueur} a mis all-in"}
    except Exception as e:
        logging.error(f"Erreur action all_in pour le joueur {id_joueur} : {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"success": False, "message": str(e)},
        )


@app.put("/action/checker/{id_joueur}", tags=["Action"])
async def checker(id_joueur: int):
    """Joue checker pour le joueur"""
    logging.info("Joue checker pour le joueur")
    try:
        action_service.checker(id_joueur)
        return {"success": True, "message": f"Joueur {id_joueur} a checké"}
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"success": False, "message": str(e)},
        )


@app.put("/action/se_coucher/{id_joueur}", tags=["Action"])
async def se_coucher(id_joueur: int):
    """Joue se_coucher pour le joueur"""
    logging.info("Joue se_coucher pour le joueur")
    return action_service.se_coucher(id_joueur)


@app.put("/action/suivre/{id_joueur}/{relance}", tags=["Action"])
async def suivre(id_joueur: int, relance: int):
    """Joue suivre pour le joueur"""
    logging.info("Joue suivre pour le joueur")
    try:
        action_service.suivre(id_joueur, relance)
        return {"success": True, "message": f"Joueur {id_joueur} a suivi {relance}"}
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"success": False, "message": str(e)},
        )


# Run the FastAPI application
if __name__ == "__main__":
    ResetDatabase().lancer()

    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5432)

    logging.info("Arret du Webservice")
