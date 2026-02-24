import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import gdown
import os
import matplotlib.pyplot as plt
import seaborn as sns


# --- CONFIGURATION & CHARGEMENT ---
@st.cache_data 
def load_data():
    file_id = '14cbUlLwF9FXAVBxa3CHe_w8Y5veh3UBd'
    url = f'https://drive.google.com/uc?id={file_id}'
    output = 'fires_clean.csv'
    
    # Téléchargement seulement s'il n'est pas déjà là
    if not os.path.exists(output):
        gdown.download(url, output, quiet=False)
    
    # Lecture (low_memory=False aide à éviter les avertissements de types)
    df = pd.read_csv(output, low_memory=False)
    
    # Optionnel : Conversion de colonnes temporelles si nécessaire
    if 'FIRE_YEAR' in df.columns:
        df['FIRE_YEAR'] = df['FIRE_YEAR'].astype(int)
        
    return df
    
# On charge le dataframe
df = load_data()

# Configuration de la page
st.set_page_config(page_title="Wildfires Analysis", layout="wide")

st.title("🔥 Analyse des Incendies aux USA")

# Barre latérale pour la navigation
page = st.sidebar.radio("Navigation", ["Accueil", "Analyse Météo", "Visualisations"])

if page == "Accueil":
    st.write("### Bienvenue dans le projet d'analyse des Wildfires")
    st.write("Ce dashboard interactif présente les résultats de notre étude sur les incendies de 1992 à 2015.")
    st.info("Utilisez le menu à gauche pour explorer les différentes étapes.")
    if st.checkbox("Afficher un aperçu des données"):
        st.dataframe(df.head(10))

# Données meteo - Lucien
elif page == "Analyse Météo":
    st.header("🌦️ Influence des conditions Météo")
    
    # 1. Définir manuellement vos 5 États (vérifiez bien l'orthographe dans votre CSV)
    top_5_states = ['CA', 'TX', 'FL', 'AZ', 'NV'] # REMPLACEZ PAR VOS 5 ÉTATS
    
    # 2. Créer le filtre limité à ces 5 choix
    st.write("### Sélectionner un État (Top 5 disposant de données météo)")
    selected_state = st.selectbox("Choisir l'État à analyser :", top_5_states)
    
    # 3. Filtrer le dataframe
    df_filtered = df[df['STATE'] == selected_state]
    
    # Information sur l'État sélectionné
    st.info(f"Affichage des données météo pour : **{selected_state}**")
    st.write(f"Nombre d'incendies analysés dans cet État : {len(df_filtered)}")
    st.divider()

    # --- La suite de vos graphiques avec df_filtered ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribution par température")
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        # Attention : on utilise df_filtered ici !
        sns.histplot(df_filtered['temp_max'], bins=30, kde=True, color='orange', ax=ax1)
        st.pyplot(fig1)

    with col2:
        st.subheader("Densité : Température vs Vent")
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        # Attention : on utilise df_filtered ici !
        hb2 = ax2.hexbin(df_filtered['temp_max'], df_filtered['vent_max'], gridsize=30, cmap='YlOrRd', mincnt=1)
        fig2.colorbar(hb2, ax=ax2, label='Densité des feux')
        st.pyplot(fig2)

    st.subheader("🔥 Sévérité : Température vs Vent (Taille moyenne)")
    df_plot = df_filtered.dropna(subset=['temp_max', 'vent_max', 'FIRE_SIZE_HECT'])
    
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    hb3 = ax3.hexbin(df_plot['temp_max'],
                    df_plot['vent_max'],
                    C=df_plot['FIRE_SIZE_HECT'],
                    reduce_C_function=np.mean,
                    gridsize=30,
                    cmap='YlOrBr',
                    mincnt=1)
    fig3.colorbar(hb3, ax=ax3, label='Taille moyenne (hectares)')
    st.pyplot(fig3)

