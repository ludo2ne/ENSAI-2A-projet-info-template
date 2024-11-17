import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.Utilisateur import Utilisateur


class UtilisateurDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux utilisateurs de la base de données"""

    def trouver_paris_par_utilisateur(id_utilisateur):
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                                SELECT p.*
                                FROM paris p
                                JOIN paris_utilisateur pu ON p.id_pari = pu.id_pari
                                WHERE pu.id_utilisateur = %(id_utilisateur)s;
                                """,
                        {"id_utilisateur": id_utilisateur},
                    )
            paris_res = cursor.fetchall()
            return paris_res
        except Exception as e:
            print(e)

    def trouver_tournois_par_utilisateur(id_utilisateur):
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT t.*
                        FROM tournoi t
                        JOIN tournois_utilisateur tu ON t.id_tournoi = tu.id_tournoi
                        WHERE tu.id_utilisateur = %(id_utilisateur)s;
                        """,
                        {"id_utilisateur": id_utilisateur},
                    )
            tournois_res = cursor.fetchall()
            return tournois_res
        except Exception as e:
            print(e)

    def instancier(self, utilisateur_bdd) -> Utilisateur:
        """Instancie un utilisateur avec ses tournois créés et ses paris.

        Parameters
        ----------
        id_utilisateur : int
            L'ID de l'utilisateur à récupérer.

        Returns
        -------
        utilisateur : Utilisateur
            Utilisateur enrichi avec ses tournois créés et ses paris.
        """

        utilisateur = Utilisateur(
            nom_utilisateur=utilisateur_bdd["pseudo"],
            mot_de_passe=utilisateur_bdd["mdp"],
            email=utilisateur_bdd["mail"],
            tournois_crees=utilisateur_bdd.get("tournois", []),  # Charge les tournois s'ils sont fournis
            points=utilisateur_bdd["points"],
            paris=utilisateur_bdd.get("paris", []),
        )
        return utilisateur



    def init():
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        CREATE TABLE IF NOT EXISTS Utilisateur (
                            id_utilisateur SERIAL PRIMARY KEY,
                            pseudo VARCHAR(30) UNIQUE,
                            mdp VARCHAR(256),
                            mail VARCHAR(50),
                            points INT DEFAULT 0,
                            paris INT[],
                            id_tournois VARCHAR(50)[]
                        );
                        """
                    )
                    connection.commit()  # Assurez-vous de confirmer la transaction
                    logging.info("Table 'utilisateur' créée ou déjà existante.")
            return True  # Indique que la table est créée ou existe déjà
        except Exception as e:
            logging.error(f"Erreur lors de la création de la table 'utilisateur': {e}")
            return False  # Indique un échec dans la création de la table


    def creer(self, utilisateur) -> bool:
        """Creation d'un utilisateur dans la base de données

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
                        INSERT INTO utilisateur(pseudo, mdp, mail, points)
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

    @log
    def trouver_par_id(self, id_utilisateur) -> Utilisateur:
        """trouver un utilisateur grace à son id

        Parameters
        ----------
        id_utilisateur : int
            numéro id du utilisateur que l'on souhaite trouver

        Returns
        -------
        utilisateur : Utilisateur
            renvoie le utilisateur que l'on cherche par id
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT *
                        FROM utilisateur
                        WHERE id_utilisateur = %(id_utilisateur)s;
                        """,
                        {"id_utilisateur": id_utilisateur},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)
            raise

        utilisateur = None
        if res:
            utilisateur = self.instancier(
                res
            )  # res est le nom de la variable dans laquelle on a stocké l'utilisateur de la dao
        return utilisateur

    @log
    def lister_tous(self) -> list[Utilisateur]:
        """lister tous les utilisateurs

        Parameters
        ----------
        None

        Returns
        -------
        liste_utilisateurs : list[Utilisateur]
            renvoie la liste de tous les utilisateurs dans la base de données
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                              "
                        "  FROM utilisateur;                        "
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)
            raise

        liste_utilisateurs = []

        if res:
            for row in res:
                utilisateur = Utilisateur(
                    id_utilisateur=row["id_utilisateur"],
                    pseudo=row["pseudo"],
                    mdp=row["mdp"],
                    mail=row["mail"],
                    tournois_crees=row["tournois_crees"],
                    points=row["points"],
                    paris=row["paris"],
                )

                liste_utilisateurs.append(utilisateur)

        return liste_utilisateurs

    @log
    def modifier(self, utilisateur) -> bool:
        """Modification d'un utilisateur dans la base de données

        Parameters
        ----------
        utilisateur : utilisateur

        Returns
        -------
        created : bool
            True si la modification est un succès
            False sinon
        """

        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE utilisateur                                      "
                        "   SET pseudo      = %(pseudo)s,                   "
                        "       mdp         = %(mdp)s,                      "
                        "       mail        = %(mail)s,                     "
                        "       tournois_crees = %(tournois_crees)s,        "
                        "       points = %(points)s,                        "
                        "       paris = %(paris)s,                          "
                        " WHERE id_utilisateur = %(id_utilisateur)s;                  ",
                        {
                            "pseudo": utilisateur.pseudo,
                            "mdp": utilisateur.mdp,
                            "mail": utilisateur.mail,
                            "tournois_crees": utilisateur.tournois_crees,
                            "points": utilisateur.points,
                            "paris": utilisateur.paris,
                            "id_utilisateur": utilisateur.id_utilisateur,
                        },
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)

        return res == 1

    @log
    def supprimer(self, utilisateur) -> bool:
        """Suppression d'un utilisateur dans la base de données

        Parameters
        ----------
        utilisateur : Utilisateur
            utilisateur à supprimer de la base de données

        Returns
        -------
            True si le utilisateur a bien été supprimé
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Supprimer le compte d'un utilisateur
                    cursor.execute(
                        "DELETE FROM utilisateur                  "
                        " WHERE id_utilisateur=%(id_utilisateur)s      ",
                        {"id_utilisateur": utilisateur.id_utilisateur},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)
            raise

        return res > 0

    @log
    def se_connecter(self, pseudo, mdp) -> Utilisateur:
        """se connecter grâce à son pseudo et son mot de passe

        Parameters
        ----------
        pseudo : str
            pseudo du utilisateur que l'on souhaite trouver
        mdp : str
            mot de passe du utilisateur

        Returns
        -------
        utilisateur : Utilisateur
            renvoie le utilisateur que l'on cherche
        """
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                           "
                        "  FROM utilisateur                      "
                        " WHERE pseudo = %(pseudo)s         "
                        "   AND mdp = %(mdp)s;              ",
                        {"pseudo": pseudo, "mdp": mdp},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        utilisateur = None

        if res:
             utilisateur = Utilisateur(
                nom_utilisateur=res["pseudo"],
                mot_de_passe=res["mdp"],  # Gardez cela uniquement si nécessaire pour des raisons techniques.
                email=res["mail"],
                tournois_crees=res.get("tournois_crees", []),
                points=res["points"],
                paris=res.get("paris", []),
    )
        return utilisateur
