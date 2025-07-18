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
    st.set_page_config(page_title="Match Your Sheets - Outil de comparaison de fichiers", layout="centered")

    custom_css = """
    <style>
    body {
        background-color: #F5F5F5;
        font-family: 'Segoe UI', sans-serif;
    }
    h1 {
        text-align: center;
        color: #333333;
        margin-bottom: 30px;
    }
    .upload-section {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 30px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
        margin: 30px auto;
        max-width: 700px;
    }
    .label {
        font-weight: 600;
        font-size: 16px;
        margin: 20px 0 5px;
        color: #444;
    }
    footer {
        text-align: center;
        margin-top: 40px;
        color: #888;
        font-size: 13px;
    }
    .center-logo {
        display: flex;
        justify-content: center;
        margin-top: 20px;
        margin-bottom: 0;
    }
    .block-container > div:nth-child(2) {
        padding-top: 0 !important;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    # Logo
    st.markdown('<div class="center-logo">', unsafe_allow_html=True)
    logo = Image.open("match-your-sheets.png")
    st.image(logo, width=500)
    st.markdown('</div>', unsafe_allow_html=True)

    # Titre
    st.markdown("<h1>Comparez 2 fichiers en quelques secondes</h1>", unsafe_allow_html=True)

    # Interface utilisateur
    with st.container():
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)

        st.markdown('<div class="label">Téléversez votre premier fichier (.xlsx)</div>', unsafe_allow_html=True)
        fichier1 = st.file_uploader("Fichier de référence", type=["xlsx"], key="fichier1")

        st.markdown('<div class="label">Téléversez le second fichier à comparer (.xlsx)</div>', unsafe_allow_html=True)
        fichier2 = st.file_uploader("Fichier à comparer", type=["xlsx"], key="fichier2")

        if fichier1 and fichier2:
            df1 = pd.read_excel(fichier1)
            df2 = pd.read_excel(fichier2)

            colonne1 = st.selectbox("🔹 Colonne de référence du premier fichier :", df1.columns)
            colonne2 = st.selectbox("🔹 Colonne de comparaison du second fichier :", df2.columns)

            if st.button("🔍 Lancer le matching"):
                df1[colonne1] = df1[colonne1].astype(str).str.strip().str.upper()
                df2[colonne2] = df2[colonne2].astype(str).str.strip().str.upper()

                # ✅ Condition mise à jour : match uniquement si la cellule n'est pas vide ou NaN
                df2["Résultat du matching"] = df2[colonne2].apply(
                    lambda x: "match" if pd.notna(x) and str(x).strip() != "" and str(x).upper() in df1[colonne1].values else "pas de match"
                )

                st.success(f"✅ Matching terminé. {df2['Résultat du matching'].value_counts().get('match', 0)} correspondance(s) trouvée(s).")
                st.dataframe(df2)

                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df2.to_excel(writer, index=False, sheet_name="Matching")
                output.seek(0)

                st.download_button(
                    label="📥 Télécharger le fichier de résultats",
                    data=output,
                    file_name="match_your_sheets_result.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<footer>© 2025 Match Your Sheets — Simplifiez vos comparaisons de données</footer>', unsafe_allow_html=True)
