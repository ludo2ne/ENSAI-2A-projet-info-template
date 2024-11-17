from dao.db_connection import DBConnection
from business_object.Utilisateur import Utilisateur

class ParisDao:
    """Classe contenant les méthodes pour accéder aux paris dans la base de données"""

    def afficher_infos_paris(nom_utilisateur):
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                                SELECT p.*
                                FROM paris p
                                JOIN paris_utilisateur pu ON p.id_pari = pu.id_pari
                                WHERE pu.nom_utilisateur = %(nom_utilisateur)s;
                                """,
                        {"nom_utilisateur": nom_utilisateur},
                    )
            paris_res = cursor.fetchall()
            return paris_res
        except Exception as e:
            print(e)

    def ajouter_un_pari(nom_utilisateur, match, equipe, montant):
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO "RocketLag".paris(nom_utilisateur, match, equipe, montant, statut)
                        VALUES (%(nom_utilisateur)s, %(match)s, %(equipe)s, %(montant)s, "En cours")
                        """,
                        {
                            "nom_utilisateur": nom_utilisateur,
                            "match": match.match_id,
                            "equipe": equipe.nom_equipe,
                            "montant": montant,
                        },
                    )
        except Exception as e:
            print(e)


    def supprimer_un_paris(self, paris) -> bool:
        """Suppression d'un pari dans la base de données

        Parameters
        ----------
        utilisateur : Utilisateur

        Returns
        -------
        created : bool
            True si la création est un succès
            False sinon
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO "RocketLag".utilisateur(pseudo, mdp, mail, points)
                        VALUES(%(pseudo)s, %(mdp)s, %(mail)s, 0)
                        RETURNING id_utilisateur;
                        """,
                        {
                            "pseudo": utilisateur.nom_utilisateur,
                            "mdp": utilisateur.mot_de_passe,
                            "mail": utilisateur.email,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            print(e)

        created = False
        if res:
            if isinstance(res["id_utilisateur"], int):
                created = True
        return created
