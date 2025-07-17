
import streamlit as st
import pandas as pd
from io import BytesIO
from PIL import Image
import yaml
from streamlit_authenticator import Authenticate
from passlib.hash import pbkdf2_sha256
import os

# --- CHARGER CONFIG ---
CONFIG_FILE = "config.yaml"

def load_config():
    with open(CONFIG_FILE, "r") as file:
        return yaml.safe_load(file)

def save_config(config):
    with open(CONFIG_FILE, "w") as file:
        yaml.dump(config, file)

config = load_config()

# --- AUTHENTICATION ---
authenticator = Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

username, authentifie, name = authenticator.login("Connexion", "main")

if authentifie:
    authenticator.logout("Se déconnecter", "sidebar")
    st.sidebar.success(f"Connecté en tant que {name}")

    st.set_page_config(page_title="AUTOMATCH - Outil de Matching de Pièces Auto", layout="centered")

    # --- CSS ---
    st.markdown("""
    <style>
    body {background-color: #F5F5F5; font-family: 'Segoe UI', sans-serif;}
    h1 {text-align: center; color: #333333; margin-bottom: 30px;}
    .upload-section {background-color: #FFF; border-radius: 12px; padding: 30px;
     box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin: 30px auto; max-width: 700px;}
    .label {font-weight: 600; font-size: 16px; margin: 20px 0 5px; color: #444;}
    footer {text-align: center; margin-top: 40px; color: #888; font-size: 13px;}
    .center-logo {display: flex; justify-content: center; margin-top: 20px; margin-bottom: 0;}
    .block-container > div:nth-child(2) {padding-top: 0 !important;}
    </style>
    """, unsafe_allow_html=True)

    # --- LOGO ---
    st.markdown('<div class="center-logo">', unsafe_allow_html=True)
    logo = Image.open("logo-automatch-bleu.png")
    st.image(logo, width=500)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<h1>Outil de Matching de Pièces Auto</h1>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📂 Fichiers", "👤 Gestion des utilisateurs"] if username == "juliette" else ["📂 Fichiers"])

    with tab1:
        with st.container():
            st.markdown('<div class="upload-section">', unsafe_allow_html=True)

            st.markdown('<div class="label">Téléversez le premier fichier Excel</div>', unsafe_allow_html=True)
            fichier1 = st.file_uploader("Téléversez le premier fichier Excel", type=["xlsx"], key="fichier1")

            st.markdown('<div class="label">Téléversez le second fichier Excel</div>', unsafe_allow_html=True)
            fichier2 = st.file_uploader("Téléversez le second fichier Excel", type=["xlsx"], key="fichier2")

            if fichier1 and fichier2:
                df1 = pd.read_excel(fichier1)
                df2 = pd.read_excel(fichier2)

                colonne1 = st.selectbox("🔹 Colonne de référence du fichier 1 :", df1.columns)
                colonne2 = st.selectbox("🔹 Colonne de référence du fichier 2 :", df2.columns)

                if st.button("🔍 Lancer le matching"):
                    df1[colonne1] = df1[colonne1].astype(str).str.strip().str.upper()
                    df2[colonne2] = df2[colonne2].astype(str).str.strip().str.upper()

                    df_matched = df1[df1[colonne1].isin(df2[colonne2])]

                    st.success(f"✅ {len(df_matched)} correspondance(s) trouvée(s).")
                    st.dataframe(df_matched)

                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df_matched.to_excel(writer, index=False, sheet_name="Matching")
                    output.seek(0)

                    st.download_button(
                        label="📥 Télécharger le fichier Excel",
                        data=output,
                        file_name="resultat_matching.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            st.markdown('</div>', unsafe_allow_html=True)

    if username == "juliette":
        with tab2:
            st.subheader("👤 Ajouter un utilisateur")
            with st.form("ajout_user"):
                new_username = st.text_input("Nom d'utilisateur")
                new_name = st.text_input("Nom complet")
                new_email = st.text_input("Adresse e-mail")
                new_password = st.text_input("Mot de passe", type="password")
                submitted = st.form_submit_button("Créer l'utilisateur")

                if submitted:
                    if new_username in config['credentials']['usernames']:
                        st.error("❌ Nom d'utilisateur déjà utilisé.")
                    else:
                        hash_pw = pbkdf2_sha256.hash(new_password)
                        config['credentials']['usernames'][new_username] = {
                            "email": new_email,
                            "name": new_name,
                            "password": hash_pw
                        }
                        save_config(config)
                        st.success("✅ Utilisateur ajouté avec succès.")

            st.subheader("👥 Utilisateurs existants")
            for user, data in config['credentials']['usernames'].items():
                st.write(f"- {user} ({data['email']})")

    st.markdown('<footer>© 2025 AUTOMATCH - Tous droits réservés</footer>', unsafe_allow_html=True)

else:
    st.warning("Veuillez vous connecter pour accéder à l’application.")

if st.session_state["username"] == "admin":
    st.subheader("🛠️ Gérer les utilisateurs existants")

    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)

        st.subheader("🛠️ Gérer les utilisateurs existants")

        for user, data in list(config['credentials']['usernames'].items()):
            with st.expander(f"{user} ({data['email']})"):
                col1, col2 = st.columns([1, 1])
                with col1:
                    new_pass = st.text_input(f"Nouveau mot de passe pour {user}", type="password", key=f"pw_{user}")
                    if st.button(f"🔑 Modifier le mot de passe", key=f"change_{user}"):
                        if new_pass:
                            config['credentials']['usernames'][user]['password'] = pbkdf2_sha256.hash(new_pass)
                            save_config(config)
                            st.success("🔄 Mot de passe mis à jour.")
                        else:
                            st.warning("Veuillez entrer un mot de passe.")
                with col2:
                    if user != "juliette":
                        if st.button(f"🗑️ Supprimer l'utilisateur", key=f"delete_{user}"):
                            del config['credentials']['usernames'][user]
                            save_config(config)
                            st.warning(f"👤 Utilisateur {user} supprimé.")
                    else:
                        st.info("Compte admin non modifiable ici.")
