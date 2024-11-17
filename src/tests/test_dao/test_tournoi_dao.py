import psycopg2


class Tournoi:
    def __init__(self, nom_tournoi, createur, officiel):
        self.nom_tournoi = nom_tournoi
        self.createur = createur
        self.officiel = officiel


class Equipe:
    def __init__(self, nom):
        self.nom = nom


class TournoiDAO:
    def __init__(self):
        # Connexion à la base de données
        self.conn = psycopg2.connect(
            host="localhost",
            database="ma_base_de_donnees",
            user="votre_utilisateur",  # Remplacez par votre utilisateur
            password="votre_mot_de_passe",  # Remplacez par votre mot de passe
        )
        self.create_tables()  # Créer les tables si elles n'existent pas

    def create_tables(self):
        """Créer les tables dans la base de données si elles n'existent pas."""
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS tournois (
                    id SERIAL PRIMARY KEY,
                    nom VARCHAR(255) NOT NULL,
                    createur VARCHAR(255) NOT NULL,
                    officiel BOOLEAN NOT NULL
                );
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS equipes (
                    id SERIAL PRIMARY KEY,
                    nom VARCHAR(255) NOT NULL
                );
            """
            )
        self.conn.commit()
        print("Tables créées avec succès (si elles n'existaient pas).")

    def ajouter_tournoi(self, tournoi):
        """Enregistre un nouveau tournoi dans la base de données."""
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO tournois (nom, createur, officiel)
                VALUES (%s, %s, %s);
            """,
                (tournoi.nom_tournoi, tournoi.createur, tournoi.officiel),
            )
        self.conn.commit()
        print(f"Tournoi '{tournoi.nom_tournoi}' ajouté avec succès.")

    def ajouter_equipe(self, equipe):
        """Ajoute une équipe à la base de données."""
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO equipes (nom)
                VALUES (%s);
            """,
                (equipe.nom,),
            )
        self.conn.commit()
        print(f"Équipe '{equipe.nom}' ajoutée à la base de données.")

    def obtenir_tournois(self):
        """Récupère tous les tournois de la base de données."""
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM tournois WHERE officiel=True;")
            return cursor.fetchall()

    def fermer_connexion(self):
        """Ferme la connexion à la base de données."""
        self.conn.close()
        print("Connexion à la base de données fermée.")


# Exemple d'utilisation
if __name__ == "__main__":
    tournoi_dao = TournoiDAO()

    # Créer un tournoi
    tournoi1 = Tournoi("Championnat de France", "Alice", True)
    tournoi_dao.ajouter_tournoi(tournoi1)

    # Créer des équipes
    equipe1 = Equipe("Team A")
    equipe2 = Equipe("Team B")

    # Ajouter les équipes
    tournoi_dao.ajouter_equipe(equipe1)
    tournoi_dao.ajouter_equipe(equipe2)

    # Obtenir les tournois
    tournois = tournoi_dao.obtenir_tournois()
    print("Tournois officiels :")
    for tournoi in tournois:
        print(tournoi)

    # Fermer la connexion
    tournoi_dao.fermer_connexion()
