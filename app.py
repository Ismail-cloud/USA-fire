import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import gdown
import os
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. CONFIGURATION DE LA PAGE (DOIT ÊTRE LA TOUTE PREMIÈRE COMMANDE) ---
st.set_page_config(page_title="Wildfires Analysis USA", layout="wide")

# --- 2. FONCTION DE CHARGEMENT DES DONNÉES (CACHE) ---
@st.cache_data 
def load_data():
    file_id = '14cbUlLwF9FXAVBxa3CHe_w8Y5veh3UBd'
    url = f'https://drive.google.com/uc?id={file_id}'
    output = 'fires_clean.csv'
    
    # Téléchargement si le fichier n'est pas localement présent sur le serveur
    if not os.path.exists(output):
        with st.spinner('Téléchargement du dataset nettoyé... Veuillez patienter.'):
            gdown.download(url, output, quiet=False)
    
    df = pd.read_csv(output, low_memory=False)
    
    # Conversion de l'année en entier pour éviter les virgules dans les filtres
    if 'FIRE_YEAR' in df.columns:
        df['FIRE_YEAR'] = df['FIRE_YEAR'].astype(int)
        
    return df

# Chargement effectif du dataframe
df = load_data()

# --- 3. STRUCTURE DE L'INTERFACE ---

st.title("🔥 Analyse des Incendies aux USA (1992-2015)")

# Barre latérale pour la navigation
page = st.sidebar.radio("Navigation", ["Accueil", "Analyse Météo", "Visualisations"])

# --- PAGE ACCUEIL ---
if page == "Accueil":
    st.write("### Bienvenue dans le projet d'analyse des Wildfires")
    st.write("""
    Ce dashboard interactif permet d'explorer les facteurs influençant les incendies de forêt.
    Nous avons croisé les données historiques du service forestier américain avec des données météo précises.
    """)
    
    st.info("Utilisez le menu à gauche pour naviguer entre l'analyse météo et les visualisations globales.")
    
    if st.checkbox("Afficher un aperçu des données brutes (10 premières lignes)"):
        st.dataframe(df.head(10))

# --- PAGE ANALY
