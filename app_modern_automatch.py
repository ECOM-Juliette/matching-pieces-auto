
import streamlit as st
import pandas as pd
from io import BytesIO
from PIL import Image

# Configuration de la page
st.set_page_config(page_title="AUTOMATCH - Outil de Matching de Pièces Auto", layout="centered")

# CSS personnalisé : fond clair, logo centré, style épuré
custom_css = """
<style>
body {
    background-color: #F5F5F5;
    font-family: 'Segoe UI', sans-serif;
}
h1 {
    text-align: center;
    color: #333333;
    margin-bottom: 20px;
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
    margin-bottom: 10px;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Logo centré
st.markdown('<div class="center-logo">', unsafe_allow_html=True)
logo = Image.open("logo-automatch-bleu.png")
st.image(logo, width=240)
st.markdown('</div>', unsafe_allow_html=True)

# Titre
st.markdown("<h1>Outil de Matching de Pièces Auto</h1>", unsafe_allow_html=True)

# Bloc principal
with st.container():
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)

    st.markdown('<div class="label">📁 Téléversez le premier fichier Excel</div>', unsafe_allow_html=True)
    fichier1 = st.file_uploader("", type=["xlsx"], key="fichier1", label_visibility="collapsed")

    st.markdown('<div class="label">📁 Téléversez le second fichier Excel</div>', unsafe_allow_html=True)
    fichier2 = st.file_uploader("", type=["xlsx"], key="fichier2", label_visibility="collapsed")

    if fichier1 and fichier2:
        df1 = pd.read_excel(fichier1)
        df2 = pd.read_excel(fichier2)

        colonne1 = st.selectbox("🔹 Choisissez la colonne de référence dans le fichier 1 :", df1.columns)
        colonne2 = st.selectbox("🔹 Choisissez la colonne de référence dans le fichier 2 :", df2.columns)

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
                file_name="résultat_matching.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    st.markdown('</div>', unsafe_allow_html=True)

# Pied de page
st.markdown('<footer>© 2025 AUTOMATCH - Tous droits réservés</footer>', unsafe_allow_html=True)
