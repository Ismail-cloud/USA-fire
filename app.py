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
elif page == "Analyse Météo":
    st.header("🌦️ Influence des conditions Météo")
    
    # 1. Correspondance des noms
    state_mapping = {
        "California": "CA",
        "Georgia": "GA",
        "Texas": "TX",
        "North Carolina": "NC",
        "Florida": "FL"
    }
    
    selected_full_name = st.selectbox("Choisir l'État à analyser :", options=list(state_mapping.keys()))
    selected_abbrev = state_mapping[selected_full_name]
    df_filtered = df[df['STATE'] == selected_abbrev]
    
    st.info(f"Analyse pour : **{selected_full_name}** ({len(df_filtered)} feux)")
    st.divider()

    # --- LIGNE 1 : L'HISTOGRAMME ---
    col_top1, col_top2 = st.columns(2)
    
    with col_top1:
        st.subheader("1. Distribution par température")
        fig1, ax1 = plt.subplots(figsize=(10, 7)) 
        sns.histplot(df_filtered['temp_max'], bins=30, kde=True, color='orange', ax=ax1)
        ax1.set_xlabel('Température Maximale (°C)')
        plt.tight_layout() 
        st.pyplot(fig1)
    
    with col_top2:
        st.write("### 📝 Observation")
        st.write(f"Dans l'état de {selected_full_name}, la majorité des incendies se déclarent à une température précise.")

    # LES HEXBINS COTE A COTE 
    st.subheader("2. Corrélations : Température vs Vent")
    col1, col2 = st.columns(2)

    with col1:
        # Graphique Densité
        fig2, ax2 = plt.subplots(figsize=(10, 7)) 
        hb2 = ax2.hexbin(df_filtered['temp_max'], df_filtered['vent_max'], gridsize=25, cmap='YlOrRd', mincnt=1)
        fig2.colorbar(hb2, ax=ax2, label='Densité des feux')
        ax2.set_title('Densité (Où sont les feux ?)')
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
        ax3.set_title('Sévérité (Taille des feux)')
        ax3.set_xlabel('Température (°C)')
        ax3.set_ylabel('Vent (km/h)')
        plt.tight_layout()
        st.pyplot(fig3)
    
    st.info(f"Affichage des données météo pour : **{selected_full_name}**")
    st.write(f"Nombre d'incendies analysés : {len(df_filtered)}")
    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribution par température")
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        sns.histplot(df_filtered['temp_max'], bins=30, kde=True, color='orange', ax=ax1)
        st.pyplot(fig1)

    with col2:
        st.subheader("Densité : Température vs Vent")
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        hb2 = ax2.hexbin(df_filtered['temp_max'], df_filtered['vent_max'], gridsize=30, cmap='YlOrRd', mincnt=1)
        fig2.colorbar(hb2, ax=ax2, label='Densité des feux')
        st.pyplot(fig2)

    st.subheader("Sévérité : Température vs Vent (Taille moyenne)")
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

