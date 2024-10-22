from service.MatchService import MatchService
import calendar


class CalendrierEvenement():

    def dictionnaire_evenement(annee):
    # Dictionnaire des événements par jour (clé = (mois, jour), valeur = événement)
    pass

    # Fonction pour afficher un calendrier d'une année complète avec des événements
    def afficher_calendrier_annee(annee, evenements):
        print(f"Calendrier pour l'année {annee} :\n")
        # Pour chaque mois de l'année
        for mois in range(1, 13):
            print(calendar.month_name[mois], annee)
            print("Lu Ma Me Je Ve Sa Di")  # En-tête des jours de la semaine

            # Obtenir le calendrier du mois sous forme de tableau
            tableau_mois = calendar.monthcalendar(annee, mois)

            # Afficher les jours du mois et ajouter des événements s'il y en a
            for semaine in tableau_mois:
                ligne = []
                for jour in semaine:
                    if jour == 0:
                        ligne.append("  ")  # Jours en dehors du mois
                    else:
                        # Ajouter un astérisque s'il y a un événement pour ce jour
                        if (mois, jour) in evenements:
                            ligne.append(f"{jour:2}*")
                        else:
                            ligne.append(f"{jour:2}")
                print(" ".join(ligne))

            print()  # Saut de ligne entre les mois

        # Liste des événements
        print("Événements de l'année :")
        for (mois, jour), evenement in evenements.items():
            print(f"{calendar.month_name[mois]} {jour} : {evenement}")



    def afficher_match_date(date):
        pass

    def rechercher_match_par_date(date):
        pass
