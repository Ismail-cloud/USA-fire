import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import gdown
import os
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Wildfires Analysis USA", layout="wide")

# FONCTION DE CHARGEMENT DES DONNÉES (CACHE) 
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

# --- PAGE ANALYSE MÉTÉO (LUCIEN) ---
elif page == "Analyse Météo":
    st.header("🌦️ Influence des conditions Météo")
    
    # Correspondance des noms d'états
    state_mapping = {
        "California": "CA",
        "Georgia": "GA",
        "Texas": "TX",
        "North Carolina": "NC",
        "Florida": "FL"
    }
    
    # Filtre par État
    st.write("### Filtrer l'analyse par État")
    selected_full_name = st.selectbox(
        "Choisir l'État à analyser :", 
        options=list(state_mapping.keys())
    )
    
    # Filtrage des données
    selected_abbrev = state_mapping[selected_full_name]
    df_filtered = df[df['STATE'] == selected_abbrev]
    
    st.info(f"Analyse en cours pour : **{selected_full_name}**")
    st.write(f"Nombre d'incendies répertoriés dans cet État : {len(df_filtered)}")
    
    st.divider()

    # --- LIGNE 1 : DISTRIBUTION ---
    col_top1, col_top2 = st.columns(2)
    
    with col_top1:
        st.subheader("1. Fréquence selon la Température")
        fig1, ax1 = plt.subplots(figsize=(10, 7))
        sns.histplot(df_filtered['temp_max'], bins=30, kde=True, color='orange', edgecolor='black', ax=ax1)
        ax1.set_xlabel('Température Maximale (°C)')
        ax1.set_ylabel('Nombre d\'incendies')
        plt.tight_layout()
        st.pyplot(fig1)
    
    with col_top2:
        st.write("### 📝 Observations")
        st.write(f"""
        En {selected_full_name}, nous observons une concentration des incendies 
        lorsque les températures maximales atteignent certains seuils critiques.
        """)

    # --- LIGNE 2 : HEXBINS CÔTE À CÔTE ---
    st.write("---")
    st.subheader("2. Corrélations : Température vs Vent")
    
    col1, col2 = st.columns(2)

    with col1:
        # Graphique Densité
        fig2, ax2 = plt.subplots(figsize=(10, 7))
        hb2 = ax2.hexbin(df_filtered['temp_max'], df_filtered['vent_max'], gridsize=25, cmap='YlOrRd', mincnt=1)
        fig2.colorbar(hb2, ax=ax2, label='Densité des feux')
        ax2.set_title('Densité (Où se déclarent les feux ?)')
        ax2.set_xlabel('Température (°C)')
        ax2.set_ylabel('Vent (km/h)')
        plt.tight_layout()
        st.pyplot(fig2)

    with col2:
        # Graphique Sévérité
        df_plot = df_filtered.dropna(subset=['temp_max', 'vent_max', 'FIRE_SIZE_HECT'])
        fig3, ax3 = plt.subplots(figsize=(10, 7))
        hb3 = ax3.hexbin(df_plot['temp_max'],
                        df_plot['vent_max'],
                        C=df_plot['FIRE_SIZE_HECT'],
                        reduce_C_function=np.mean,
                        gridsize=25,
                        cmap='YlOrBr',
                        mincnt=1)
        fig3.colorbar(hb3, ax=ax3, label='Taille moy. (ha)')
        ax3.set_title('Sévérité (Taille moyenne des feux)')
        ax3.set_xlabel('Température (°C)')
        ax3.set_ylabel('Vent (km/h)')
        plt.tight_layout()
        st.pyplot(fig3)
