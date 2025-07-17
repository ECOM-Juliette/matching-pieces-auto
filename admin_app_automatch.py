
import streamlit as st
import yaml
import os
from streamlit_authenticator import Authenticate
from passlib.hash import pbkdf2_sha256
import json

st.set_page_config(page_title="Admin - AUTOMATCH", layout="centered")

st.title("🔐 Interface Admin - AUTOMATCH")

CREDENTIALS_PATH = "users_credentials.yaml"

# Fonction de chargement
def load_credentials():
    if os.path.exists(CREDENTIALS_PATH):
        with open(CREDENTIALS_PATH, "r") as f:
            return yaml.safe_load(f)
    else:
        return {"credentials": {"usernames": {}}}

# Fonction d'enregistrement
def save_credentials(config):
    with open(CREDENTIALS_PATH, "w") as f:
        yaml.dump(config, f)

# Interface admin
config = load_credentials()

st.subheader("➕ Ajouter un nouvel utilisateur")
new_email = st.text_input("Adresse email")
new_name = st.text_input("Nom d'utilisateur")
new_password = st.text_input("Mot de passe", type="password")

if st.button("Créer l'utilisateur"):
    if new_email in config["credentials"]["usernames"]:
        st.error("Cet utilisateur existe déjà.")
    else:
        config["credentials"]["usernames"][new_email] = {
            "email": new_email,
            "name": new_name,
            "password": pbkdf2_sha256.hash(new_password)
        }
        save_credentials(config)
        st.success("Nouvel utilisateur créé !")

st.markdown("---")
st.subheader("🛠️ Gérer les utilisateurs existants")

emails = list(config["credentials"]["usernames"].keys())
if emails:
    selected = st.selectbox("Sélectionner un utilisateur", emails)

    if st.button("🗑️ Supprimer cet utilisateur"):
        del config["credentials"]["usernames"][selected]
        save_credentials(config)
        st.warning(f"Utilisateur {selected} supprimé.")

    new_pw = st.text_input("Nouveau mot de passe", type="password")
    if st.button("🔁 Modifier le mot de passe"):
        config["credentials"]["usernames"][selected]["password"] = pbkdf2_sha256.hash(new_pw)
        save_credentials(config)
        st.success("Mot de passe mis à jour.")
else:
    st.info("Aucun utilisateur enregistré pour le moment.")
