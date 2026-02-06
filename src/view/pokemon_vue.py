from InquirerPy import inquirer

from client.pokemon_client import PokemonClient
from view.vue_abstraite import VueAbstraite


class PokemonVue(VueAbstraite):
    """Vue qui affiche :
    - la liste des types de pokemons dans un premier temps
    - la liste des pokemons du type choisi dans un seconde temps
    """

    def choisir_menu(self):
        pokemon_client = PokemonClient()

        pokemon_types = pokemon_client.get_pokemon_types()
        pokemon_types.append("Retour au Menu Joueur")

        choix = inquirer.select(
            message="Choisissez un type de Pokemon : ",
            choices=pokemon_types,
        ).execute()

        if choix == "Retour au Menu Joueur":
            from view.menu_joueur_vue import MenuJoueurVue

            return MenuJoueurVue()

        from view.menu_joueur_vue import MenuJoueurVue

        pokemons_str = f"Liste des pokemons du type {choix} :\n\n"
        pokemons_str += str(pokemon_client.get_all_pokemon_by_types(choix))
        return MenuJoueurVue(pokemons_str)
