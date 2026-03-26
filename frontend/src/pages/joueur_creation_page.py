# frontend/pages/joueur_creation.py
import requests
import streamlit as st

API_URL = st.secrets.get("API_URL", "http://localhost:5000")


st.title("➕ Création d'un joueur")
if st.button("⬅️ Retour au menu"):
    st.switch_page("pages/main_page.py")

pseudo = st.text_input("Pseudo")
mdp = st.text_input("Mot de passe", type="password")
age = st.number_input("Âge", min_value=1, max_value=120)
mail = st.text_input("Email")
fan_pokemon = st.checkbox("Fan de Pokémon ?")

if st.button("Créer le joueur"):
    joueur = {
        "pseudo": pseudo,
        "mdp": mdp,
        "age": age,
        "mail": mail,
        "fan_pokemon": fan_pokemon,
    }
    try:
        r = requests.post(f"{API_URL}/joueur/", json=joueur)
        if r.status_code == 200:
            st.success(f"Joueur {pseudo} créé avec succès ! 🎉")
        else:
            try:
                error_detail = r.json().get("detail", r.text)
            except ValueError:
                error_detail = r.text
            st.error(
                f"Erreur lors de la création.  \nStatut : {r.status_code}  \nDétail : {error_detail}"
            )
    except requests.RequestException as e:
        st.error(f"Impossible de contacter le serveur API : {e}")
