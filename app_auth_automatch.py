import streamlit as st 
import pandas as pd
from io import BytesIO
from PIL import Image
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

# Chargement de la configuration
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Authentification
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

name, authentication_status, username = authenticator.login("Se connecter", location="main")

if authentication_status is False:
    st.error("Nom d’utilisateur ou mot de passe incorrect")
elif authentication_status is None:
    st.warning("Veuillez entrer vos identifiants")
elif authentication_status:
    st.success(f"Bienvenue {name} 👋")

    # Configuration de la page
    st.set_page_config(page_title="AUTOMATCH - Outil de Matching de Pièces Auto", layout="centered")

    # CSS personnalisé
    custom_css = """
    <style>
    body {
        background-color: #F5F5F5;
        font-family: 'Segoe UI', sans-serif;
    }
    h1 {
        text-align: center;
        color: #333333;
