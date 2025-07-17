import streamlit as st
import yaml
import streamlit_authenticator as stauth
import os

# Charger la configuration depuis config.yaml
with open("config.yaml") as file:
    config = yaml.safe_load(file)

# Authentification avec Streamlit Authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

# Interface de connexion
st.title("Admin - Gestion des Utilisateurs")

name, authentication_status, username = authenticator.login("Se connecter", location="main")

# Accès uniquement pour l'admin
if authentication_status:
    user_data = config["credentials"]["usernames"].get(username, {})
    role = user_data.get("role", "user")

    if role != "admin":
        st.error("⛔️ Vous n'avez pas accès à cette page.")
        st.stop()

    st.success(f"Bienvenue {name} (admin)")

    st.subheader("🔍 Gérer les utilisateurs existants")

    for user, data in config['credentials']['usernames'].items():
        if user != username:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"**{data['name']}** ({user})")
            with col2:
                if st.button("🚫 Supprimer", key=f"suppr_{user}"):
                    config['credentials']['usernames'].pop(user)
                    with open("config.yaml", "w") as f:
                        yaml.safe_dump(config, f)
                    st.success(f"Utilisateur {user} supprimé.")
                    st.experimental_rerun()

    st.subheader("🔄 Mettre à jour un mot de passe")
    user_to_update = st.selectbox("Choisir l'utilisateur", list(config['credentials']['usernames'].keys()))
    new_password = st.text_input("Nouveau mot de passe", type="password")
    if st.button("🔄 Modifier"):
        if new_password:
            hashed_pw = stauth.Hasher([new_password]).generate()[0]
            config['credentials']['usernames'][user_to_update]['password'] = hashed_pw
            with open("config.yaml", "w") as f:
                yaml.safe_dump(config, f)
            st.success("Mot de passe mis à jour !")
        else:
            st.warning("Veuillez entrer un nouveau mot de passe.")

    st.subheader("➕ Ajouter un nouvel utilisateur")
    new_email = st.text_input("Email")
    new_name = st.text_input("Nom complet")
    new_password_raw = st.text_input("Mot de passe", type="password")
    if st.button("➕ Créer l'utilisateur"):
        if new_email and new_name and new_password_raw:
            if new_email in config['credentials']['usernames']:
                st.warning("Cet utilisateur existe déjà.")
            else:
                hashed_new_pw = stauth.Hasher([new_password_raw]).generate()[0]
                config['credentials']['usernames'][new_email] = {
                    "email": new_email,
                    "name": new_name,
                    "password": hashed_new_pw,
                    "role": "user"  # par défaut non admin
                }
                with open("config.yaml", "w") as f:
                    yaml.safe_dump(config, f)
                st.success("Nouvel utilisateur créé avec succès !")
                st.experimental_rerun()

elif authentication_status is False:
    st.error("Nom d’utilisateur ou mot de passe incorrect")

elif authentication_status is None:
    st.warning("Veuillez entrer vos identifiants")
