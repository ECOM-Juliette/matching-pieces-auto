
import streamlit as st
import pandas as pd
from io import BytesIO
from PIL import Image

# Configuration de la page
st.set_page_config(page_title="AUTOMATCH - Matching Pièces Auto", layout="centered")

# Appliquer un design moderne avec fond clair et encarts stylés
modern_css = """
<style>
body {
    background-color: #F5F5F5;
    font-family: 'Segoe UI', sans-serif;
}

h1 {
    text-align: center;
    color: #333333;
}

.upload-section {
    background-color: #FFFFFF;
    border-radius: 12px;
    padding: 30px;
    box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
    margin-top: 20px;
}

.label {
    font-weight: 600;
    font-size: 16px;
    margin-bottom: 10px;
    color: #444;
    display: flex;
    align-items: center;
    gap: 10px;
}

footer {
    text-align: center;
    margin-top: 40px;
    color: #888;
    font-size: 13px;
}
</style>
"""
st.markdown(modern_css, unsafe_allow_html=True)

# Logo centré
logo = Image.open("logo-automatch.png")
st.image(logo, width=200)

# Titre
st.markdown("<h1>AUTOMATCH – Outil de Matching de Pièces Auto</h1>", unsafe_allow_html=True)

# Section principale
with st.container():
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)

    # Upload fichiers
    st.markdown('<div class="label">📂 Téléversez le premier fichier Excel</div>', unsafe_allow_html=True)
    fichier1 = st.file_uploader("", type=["xlsx"], key="fichier1")

    st.markdown('<div class="label">📂 Téléversez le second fichier Excel</div>', unsafe_allow_html=True)
    fichier2 = st.file_uploader("", type=["xlsx"], key="fichier2")

    if fichier1 and fichier2:
        df1 = pd.read_excel(fichier1)
        df2 = pd.read_excel(fichier2)

        colonne1 = st.selectbox("📌 Colonne de référence dans le fichier 1", df1.columns)
        colonne2 = st.selectbox("📌 Colonne de référence dans le fichier 2", df2.columns)

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
                label="📥 Télécharger les résultats",
                data=output,
                file_name="resultat_matching.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<footer>© 2025 AUTOMATCH - Tous droits réservés</footer>', unsafe_allow_html=True)
