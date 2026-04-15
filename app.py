import streamlit as st
import pandas as pd
import plotly.express as px

# Configuration de la page
st.set_page_config(page_title="HospitData Ultra Pro", layout="wide", page_icon="🏥")

# --- INITIALISATION DE LA BASE DE DONNÉES ---
if 'db_patients' not in st.session_state:
    # Structure complète avec toutes les variables demandées
    st.session_state.db_patients = pd.DataFrame(columns=[
        'Heure', 'Patient', 'Âge', 'Groupe Sanguin', 'Taille (cm)', 'Poids (kg)', 
        'IMC', 'Antécédents', 'Allergies', 'Température (°C)', 'Pouls (BPM)', 'Douleur', 'Risque'
    ])

# --- INTERFACE ---
st.title("HospitData : Système de Gestion Clinique")

tab1, tab2 = st.tabs(["Saisie des Données", "Tableau de Bord & Analyse"])

with tab1:
    st.subheader("📝 Nouvelle Fiche Patient")
    with st.form("form_complet", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        
        with c1:
            st.markdown("**Identité**")
            nom = st.text_input("Nom du Patient")
            age = st.number_input("Âge", 0, 120, 30)
            groupe_sanguin = st.selectbox("Groupe Sanguin", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Inconnu"])
            
        with c2:
            st.markdown("**⚖️ Morphologie**")
            taille = st.number_input("Taille (cm)", 50, 250, 170)
            poids = st.number_input("Poids (kg)", 2.0, 250.0, 70.0)
            st.caption("L'IMC est calculé automatiquement à l'enregistrement.")
            
        with c3:
            st.markdown("**Antécédents & Sécurité**")
            maladies = st.multiselect("Maladies Chroniques", ["Diabète", "Hypertension", "Asthme", "Insuffisance Cardiaque"])
            allergies = st.text_input("Allergies spécifiques")
            
        st.divider()
        st.markdown("**Signes Vitaux actuels**")
        v1, v2, v3 = st.columns(3)
        temp = v1.number_input("Température (°C)", 34.0, 43.0, 37.0, step=0.1)
        pouls = v2.number_input("Pouls (BPM)", 30, 220, 75)
        douleur = v3.select_slider("Niveau de Douleur", options=range(11))

        submit = st.form_submit_button("Enregistrer le dossier complet")
        
        if submit:
            if not nom:
                st.error("Veuillez entrer le nom du patient.")
            else:
                # CALCULS AUTOMATIQUES
                # 1. IMC
                imc = round(poids / ((taille/100)**2), 1)
                
                # 2. Score de Risque Intelligent
                risque = "🟢 Stable"
                if temp > 38.5 or douleur > 7 or (age > 75 and temp > 38.0):
                    risque = "🔴 Critique"
                elif temp > 37.8 or len(maladies) > 0 or imc > 30:
                    risque = "🟠 À surveiller"

                # Création de la ligne
                nouvelle_ligne = pd.DataFrame([{
                    'Heure': pd.Timestamp.now().strftime('%H:%M:%S'),
                    'Patient': nom,
                    'Âge': age,
                    'Groupe Sanguin': groupe_sanguin,
                    'Taille (cm)': taille,
                    'Poids (kg)': poids,
                    'IMC': imc,
                    'Antécédents': ", ".join(maladies) if maladies else "Aucun",
                    'Allergies': allergies if allergies else "Aucune",
                    'Température (°C)': temp,
                    'Pouls (BPM)': pouls,
                    'Douleur': douleur,
                    'Risque': risque
                }])
                
                st.session_state.db_patients = pd.concat([st.session_state.db_patients, nouvelle_ligne], ignore_index=True)
                st.success(f"Dossier enregistré pour {nom} (IMC: {imc})")
                st.balloons()

with tab2:
    st.subheader("Analyse des Données en Temps Réel")
    df = st.session_state.db_patients

    if not df.empty:
        # Indicateurs clés
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Patients", len(df))
        m2.metric("Cas Critiques (🔴)", len(df[df['Risque'] == "🔴 Critique"]))
        m3.metric("Temp. Moyenne", f"{round(df['Température (°C)'].mean(), 1)} °C")
        m4.metric("IMC Moyen", round(df['IMC'].mean(), 1))

        st.divider()
        
        # Diagrammes
        c1, c2 = st.columns(2)
        
        with c1:
            st.write("**Analyse de la Température par Risque**")
            fig_temp = px.bar(df, x='Patient', y='Température (°C)', color='Risque',
                             color_discrete_map={"🟢 Stable": "green", "🟠 À surveiller": "orange", "🔴 Critique": "red"})
            st.plotly_chart(fig_temp, use_container_width=True)
            
        with c2:
            st.write("**Répartition des Groupes Sanguins**")
            fig_pie = px.pie(df, names='Groupe Sanguin', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_pie, use_container_width=True)

        # Tableau des données
        st.write("**Registre Complet des Patients**")
        st.dataframe(df, use_container_width=True)

        # Exportation
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Télécharger le registre complet (CSV)",
            data=csv,
            file_name='rapport_HospitData_complet.csv',
            mime='text/csv',
        )
    else:
        st.info("Aucune donnée enregistrée. Veuillez utiliser l'onglet Saisie.")

# --- BARRE LATÉRALE (Sidebar) ---
st.sidebar.title("Administration")
if st.sidebar.button("Réinitialiser la base"):
    st.session_state.db_patients = pd.DataFrame(columns=st.session_state.db_patients.columns)
    st.rerun()

st.sidebar.divider()
st.sidebar.write("**HospitData v2.0**")
st.sidebar.caption("Outil de démonstration hospitalière")
