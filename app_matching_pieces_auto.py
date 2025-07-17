import streamlit as st
import pandas as pd
from io import BytesIO
from pathlib import Path
from PIL import Image

# -------------------------
# Config page
# -------------------------
st.set_page_config(
    page_title="AUTOMATCH - Matching Pièces Auto",
    layout="centered"
)

# -------------------------
# Couleur de fond personnalisée
# (cible les bons conteneurs Streamlit)
# -------------------------
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #5E7A8A;
    }
    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------
# Logo
# -------------------------
LOGO_PATH = Path(__file__).parent / "logo-automatch.png"
if LOGO_PATH.exists():
    st.image(str(LOGO_PATH), width=250)
else:
    st.write("⚠️ Logo manquant (logo-automatch.png).")

st.title("🔧 AUTOMATCH – Outil de Matching de Pièces Auto")

# -------------------------
# Upload fichiers
# -------------------------
fichier1 = st.file_uploader("📁 Téléversez le premier fichier Excel", type=["xlsx"])
fichier2 = st.file_uploader("📁 Téléversez le second fichier Excel", type=["xlsx"])

if fichier1 and fichier2:
    df1 = pd.read_excel(fichier1)
    df2 = pd.read_excel(fichier2)

    st.subheader("🔍 Sélectionnez les colonnes à comparer")
    colonne1 = st.selectbox("Colonne de référence dans le fichier 1", df1.columns)
    colonne2 = st.selectbox("Colonne de référence dans le fichier 2", df2.columns)

    if st.button("▶️ Lancer le matching"):
        # Normalisation
        df1[colonne1] = df1[colonne1].astype(str).str.strip().str.upper()
        df2[colonne2] = df2[colonne2].astype(str).str.strip().str.upper()

        # Matching
        df_matched = df1[df1[colonne1].isin(df2[colonne2])]

        st.success(f"✅ {len(df_matched)} correspondance(s) trouvée(s).")
        st.dataframe(df_matched)

        # Export Excel
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
