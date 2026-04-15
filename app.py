import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px # Pour des graphiques interactifs

st.set_page_config(page_title="HospitData Analytics", layout="wide")

# --- SIMULATION DE BASE DE DONNÉES ---
if 'db_patients' not in st.session_state:
    # On crée quelques données de départ pour que ce ne soit pas vide
    data = {
        'Heure': pd.date_range(start='2026-04-15', periods=5, freq='h'),
        'Patient': ['Patient A', 'Patient B', 'Patient C', 'Patient D', 'Patient E'],
        'Température': [37.2, 38.5, 36.9, 39.1, 37.5],
        'Douleur': [2, 5, 1, 8, 3]
    }
    st.session_state.db_patients = pd.DataFrame(data)

# --- INTERFACE ---
st.title("🏥 HospitData : Collecte & Analyse")

tab1, tab2 = st.tabs(["📥 Saisie des Données", "📊 Tableau de Bord (Diagrammes)"])

with tab1:
    st.subheader("Nouveau Relevé Médical")
    with st.form("form_hopital"):
        nom = st.text_input("Nom du Patient")
        temp = st.number_input("Température (°C)", 35.0, 42.0, 37.0)
        douleur = st.slider("Niveau de Douleur", 0, 10)
        submit = st.form_submit_button("Enregistrer")
        
        if submit:
            nouvelle_ligne = pd.DataFrame({'Heure': [pd.Timestamp.now()], 'Patient': [nom], 'Température': [temp], 'Douleur': [douleur]})
            st.session_state.db_patients = pd.concat([st.session_state.db_patients, nouvelle_ligne], ignore_index=True)
            st.success("Donnée ajoutée au système !")

with tab2:
    st.subheader("Analyse des Constantes en Temps Réel")
    df = st.session_state.db_patients

    # Indicateurs clés (Metrics)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Patients", len(df))
    col2.metric("Temp. Moyenne", f"{round(df['Température'].mean(), 1)} °C")
    col3.metric("Alerte Douleur (>7)", len(df[df['Douleur'] > 7]))

    # Diagrammes
    st.divider()
    c1, c2 = st.columns(2)
    
    with c1:
        st.write("**Évolution de la Température**")
        fig_temp = px.line(df, x='Heure', y='Température', markers=True, color_discrete_sequence=['red'])
        st.plotly_chart(fig_temp, use_container_width=True)
        
    with c2:
        st.write("**Répartition des Niveaux de Douleur**")
        fig_bar = px.bar(df, x='Patient', y='Douleur', color='Douleur', color_continuous_scale='Viridis')
        st.plotly_chart(fig_bar, use_container_width=True)

    st.write("**Tableau des données brutes**")
    st.dataframe(df, use_container_width=True)
