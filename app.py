import streamlit as st
import pandas as pd
import plotly.express as px

# Configuration de la page
st.set_page_config(page_title="Wildfires Analysis", layout="wide")

st.title("🔥 Analyse des Incendies aux USA")

# Barre latérale pour la navigation
page = st.sidebar.radio("Navigation", ["Accueil", "Exploration des données", "Visualisations"])

if page == "Accueil":
    st.write("### Bienvenue dans le projet d'analyse des Wildfires")
    st.write("Ce dashboard interactif présente les résultats de notre étude sur les incendies de 1992 à 2015.")
    st.info("Utilisez le menu à gauche pour explorer les différentes étapes.")

elif page == "Exploration des données":
    st.header("🔍 Exploration et Qualité des données")
    st.write("Cette section présente l'analyse initiale des colonnes et les taux de valeurs manquantes.")
    
    # Ici vous pourrez ajouter vos fonctions d'analyse de colonnes
    # Exemple : st.write(df.isna().mean() * 100)

elif page == "Visualisations":
    st.header("📊 Graphiques et Cartographies")
    st.write("Analyse temporelle et géographique des incendies.")
