import sqlite3

############### on va définir ici la classe tornoi avec ses 3 fonctiuonnalitées et qui va me permettre de gérer
############### des tournois qui seront crées par mes utilisateurs viusiteurs ( uniquement). il est à noter que pour les matchs offiels,
################ cela se fezra directement via Api.

class Tournoi:
    def __init__(self, nom_tournoi, createur, officiel=False, db_name='tournois.db'):
        self.nom_tournoi = nom_tournoi
        self.createur = createur
        self.officiel = officiel 
        self.equipes = [] 
        self.matchs = []  
        self.conn = sqlite3.connect(db_name) 

    def ajouter_equipes(self, liste_equipes):
        for equipe in liste_equipes:
            self.equipes.append(equipe)
            self.enregistrer_equipe_bdd(equipe) 
        print(f"Équipes ajoutées au tournoi {self.nom_tournoi}.")

    def inscrire_equipe(self, equipe):
        if self.officiel:
            print(f"Équipe {equipe.nom} inscrite dans un tournoi officiel.")
            self.enregistrer_tournoi(self.nom_tournoi, True)
        else:
            print(f"Équipe {equipe.nom} inscrite dans un tournoi personnel.")
            self.enregistrer_tournoi(self.nom_tournoi, False)
        
        self.equipes.append(equipe)

    def enregistrer_tournoi(self, nom_tournoi, officiel):
        print(f"Tournoi {nom_tournoi} enregistré avec officiel={officiel}.")

    def suivre_resultats(self, equipe1, equipe2, score1, score2):
        if equipe1 not in self.equipes or equipe2 not in self.equipes:
            print("Les équipes doivent être inscrites au tournoi.")
            return
        
        gagnant = equipe1 if score1 > score2 else equipe2
        match = {
            'equipe1': equipe1.nom,
            'score1': score1,
            'equipe2': equipe2.nom,
            'score2': score2,
            'gagnant': gagnant.nom
        }
        self.matchs.append(match)
        print(f"Match joué: {equipe1.nom} {score1} - {equipe2.nom} {score2}. Gagnant: {gagnant.nom}")
        return gagnant

    def afficher_classement(self):
        classement = {equipe.nom: 0 for equipe in self.equipes}
        for match in self.matchs:
            classement[match['gagnant']] += 1  

        classement_trie = sorted(classement.items(), key=lambda x: x[1], reverse=True)
        print("\nClassement final :")
        for rang, (equipe_nom, victoires) in enumerate(classement_trie):
            print(f"{rang + 1}. {equipe_nom} - {victoires} victoires")

        return classement_trie 

    def gagnant_tournoi(self):
        classement = self.afficher_classement()

        if classement:
            gagnant_final = classement[0][0]  
            print(f"\nLe gagnant du tournoi {self.nom_tournoi} est : {gagnant_final}")
            return gagnant_final
        else:
            print("Aucune équipe n'a participé au tournoi.")
            return None














