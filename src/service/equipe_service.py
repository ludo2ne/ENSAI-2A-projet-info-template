from business_object.Equipe import Equipe


class EquipeService:

    def instancier(self, equipe_bdd):
        equipe = Equipe(
            nom_equipe=equipe_bdd["nom_equipe"],
            shots=equipe_bdd["shots"],
            goals=equipe_bdd["goals"],
            saves=equipe_bdd["saves"],
            assists=equipe_bdd["assists"],
            score=equipe_bdd["scores"],
            shooting_percentage=equipe_bdd["shooting_percentage"],
        )
        return equipe
