import streamlit as st
import pandas as pd
import plotly.express as px
import random

# Configuration de la page
st.set_page_config(page_title="HospitData Ultra Pro", layout="wide", page_icon="🏥")

# --- INITIALISATION DE LA BASE DE DONNÉES AVEC 10 PATIENTS PRÉ-REMPLIS ---
if 'db_patients' not in st.session_state:
    # Liste de noms pour la simulation
    noms = ["Jean Dupont", "Marie Claire", "Ahmed Bakari", "Sophie Martin", "Luc Durand", 
            "Elena Rossi", "Marc Lefebvre", "Alice Wong", "Paul Moreau", "Yasmine Traoré"]
    groupes = ["A+", "O-", "B+", "AB+", "A-", "O+", "B-", "A+", "O+", "AB-"]
    
    pre_data = []
    for i in range(10):
        t = random.uniform(36.5, 39.5) # Température aléatoire
        p = random.randint(60, 110)    # Pouls aléatoire
        d = random.randint(0, 9)       # Douleur aléatoire
        age = random.randint(18, 85)   # Âge aléatoire
        taille = random.randint(155, 190)
        poids = random.uniform(55.0, 95.0)
        imc = round(poids / ((taille/100)**2), 1)
        
        # Calcul du risque pour les données de départ
        risque = "🟢 Stable"
        if t > 38.5 or d > 7: risque = "🔴 Critique"
        elif t > 37.8 or imc > 30: risque = "🟠 À surveiller"

        pre_data.append({
            'Heure': f"0{9+i}:00:00",
            'Patient': noms[i],
            'Âge': age,
            'Groupe Sanguin': groupes[i],
            'Taille (cm)': taille,
            'Poids (kg)': round(poids, 1),
            'IMC': imc,
            'Antécédents': random.choice(["Aucun", "Hypertension", "Diabète", "Asthme"]),
            'Allergies': random.choice(["Aucune", "Pénicilline", "Latex"]),
            'Température (°C)': round(t, 1),
            'Pouls (BPM)': p,
            'Douleur': d,
            'Risque': risque
        })
    
    st.session_state.db_patients = pd.DataFrame(pre_data)

# --- INTERFACE ---
st.title("🏥 HospitData : Système de Collecte & Analyse Médicale")

tab1, tab2 = st.tabs(["📥 Saisie des Données", "📊 Tableau de Bord & Analyse"])

with tab1:
    st.subheader("📝 Nouvelle Fiche Patient")
    with st.form("form_complet", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        
        with c1:
            st.markdown("**👤 Identité**")
            nom_input = st.text_input("Nom du Patient")
            age_input = st.number_input("Âge", 0, 120, 30)
            gs_input = st.selectbox("Groupe Sanguin", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Inconnu"])
            
        with c2:
            st.markdown("**⚖️ Morphologie**")
            t_input = st.number_input("Taille (cm)", 50, 250, 170)
            p_input = st.number_input("Poids (kg)", 2.0, 250.0, 70.0)
            
        with c3:
            st.markdown("**📜 Antécédents & Sécurité**")
            m_input = st.multiselect("Maladies Chroniques", ["Diabète", "Hypertension", "Asthme", "Insuffisance Cardiaque"])
            a_input = st.text_input("Allergies spécifiques")
            
        st.divider()
        st.markdown("**🌡️ Signes Vitaux actuels**")
        v1, v2, v3 = st.columns(3)
        temp_input = v1.number_input("Température (°C)", 34.0, 43.0, 37.0, step=0.1)
        pouls_input = v2.number_input("Pouls (BPM)", 30, 220, 75)
        douleur_input = v3.select_slider("Niveau de Douleur", options=range(11))

        if st.form_submit_button("✅ Enregistrer le dossier"):
            if not nom_input:
                st.error("Nom obligatoire.")
            else:
                imc_calc = round(p_input / ((t_input/100)**2), 1)
                risque_calc = "🟢 Stable"
                if temp_input > 38.5 or douleur_input > 7: risque_calc = "🔴 Critique"
                elif temp_input > 37.8 or len(m_input) > 0: risque_calc = "🟠 À surveiller"

                nouvelle_ligne = pd.DataFrame([{
                    'Heure': pd.Timestamp.now().strftime('%H:%M:%S'),
                    'Patient': nom_input, 'Âge': age_input, 'Groupe Sanguin': gs_input,
                    'Taille (cm)': t_input, 'Poids (kg)': p_input, 'IMC': imc_calc,
                    'Antécédents': ", ".join(m_input) if m_input else "Aucun",
                    'Allergies': a_input if a_input else "Aucune",
                    'Température (°C)': temp_input, 'Pouls (BPM)': pouls_input,
                    'Douleur': douleur_input, 'Risque': risque_calc
                }])
                st.session_state.db_patients = pd.concat([st.session_state.db_patients, nouvelle_ligne], ignore_index=True)
                st.success("Dossier enregistré !")
                st.balloons()

with tab2:
    st.subheader("📊 Analyse des Données (10+ Patients)")
    df = st.session_state.db_patients

    if not df.empty:
        # Indicateurs
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Patients", len(df))
        m2.metric("Cas Critiques", len(df[df['Risque'] == "🔴 Critique"]))
        m3.metric("Temp. Moyenne", f"{round(df['Température (°C)'].mean(), 1)} °C")
        m4.metric("IMC Moyen", round(df['IMC'].mean(), 1))

        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            fig_temp = px.bar(df, x='Patient', y='Température (°C)', color='Risque',
                             color_discrete_map={"🟢 Stable": "green", "🟠 À surveiller": "orange", "🔴 Critique": "red"})
            st.plotly_chart(fig_temp, use_container_width=True)
        with c2:
            fig_pie = px.pie(df, names='Groupe Sanguin', hole=0.4, title="Stock Sanguin Estimé")
            st.plotly_chart(fig_pie, use_container_width=True)

        st.dataframe(df, use_container_width=True)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Télécharger Rapport CSV", csv, "rapport_HospitData.csv", "text/csv")

# --- BARRE LATÉRALE ---
st.sidebar.title("🛠️ Administration")
if st.sidebar.button("🗑️ Vider la base"):
    st.session_state.db_patients = pd.DataFrame(columns=st.session_state.db_patients.columns)
    st.rerun()
    import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import random

# Configuration
st.set_page_config(page_title="HospitData Analytics Pro", layout="wide", page_icon="🏥")

# --- INITIALISATION (10 PATIENTS) ---
if 'db_patients' not in st.session_state:
    noms = ["Jean Dupont", "Marie Claire", "Ahmed Bakari", "Sophie Martin", "Luc Durand", 
            "Elena Rossi", "Marc Lefebvre", "Alice Wong", "Paul Moreau", "Yasmine Traoré"]
    pre_data = []
    for i in range(10):
        age = random.randint(18, 85)
        temp = random.uniform(36.2, 39.8)
        poids = random.uniform(50, 100)
        taille = random.randint(155, 190)
        imc = round(poids / ((taille/100)**2), 1)
        douleur = random.randint(0, 10)
        pre_data.append({
            'Heure': f"0{9+i}:00", 'Patient': noms[i], 'Âge': age, 
            'Poids (kg)': round(poids, 1), 'Taille (cm)': taille, 'IMC': imc,
            'Température': round(temp, 1), 'Douleur': douleur,
            'Risque': "🔴 Critique" if temp > 38.5 else "🟢 Stable"
        })
    st.session_state.db_patients = pd.DataFrame(pre_data)

st.title("🏥 HospitData : Analyse & Régression Linéaire")

tab1, tab2, tab3 = st.tabs(["📥 Saisie", "📊 Graphiques", "🧬 Modèles Prédictifs (IA)"])

# --- TAB 1 & 2 (Identiques à avant mais simplifiés ici pour la lecture) ---
with tab1:
    st.info("Utilisez ce formulaire pour ajouter de nouveaux patients à l'étude.")
    # ... (Garder votre formulaire de saisie ici)

with tab2:
    df = st.session_state.db_patients
    st.subheader("Visualisation Descriptive")
    c1, c2 = st.columns(2)
    c1.plotly_chart(px.bar(df, x='Patient', y='Température', color='Risque'), use_container_width=True)
    c2.plotly_chart(px.scatter(df, x='Âge', y='IMC', size='Douleur', color='Risque'), use_container_width=True)

# --- NOUVEAU : TAB 3 - RÉGRESSION LINÉAIRE ---
with tab3:
    st.header("🔬 Analyse Statistique Avancée")
    df = st.session_state.db_patients
    
    if len(df) > 2:
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("1. Régression Linéaire Simple")
            st.write("Objectif : Prédire la **Température** en fonction de l'**Âge**.")
            
            # Calcul de la régression simple (y = ax + b) avec Numpy
            x = df['Âge']
            y = df['Température']
            a, b = np.polyfit(x, y, 1)
            
            fig_reg = px.scatter(df, x='Âge', y='Température', trendline="ols", 
                                 title=f"Équation : Temp = {a:.3f}*Âge + {b:.2f}")
            st.plotly_chart(fig_reg, use_container_width=True)
            st.write(f"💡 **Interprétation :** Pour chaque année d'âge supplémentaire, la température varie de {a:.3f}°C.")

        with col_right:
            st.subheader("2. Régression Linéaire Multiple (Concept)")
            st.write("Objectif : Estimer l'**Indice de Fragilité** (combiné).")
            
            # Simulation d'une régression multiple (Score = 0.5*Âge + 0.2*IMC + 0.3*Douleur)
            df['Score_Fragilité'] = (df['Âge'] * 0.5) + (df['IMC'] * 0.2) + (df['Douleur'] * 0.3)
            
            fig_multi = px.scatter_3d(df, x='Âge', y='IMC', z='Douleur', color='Score_Fragilité',
                                     title="Modèle 3D de Régression Multiple")
            st.plotly_chart(fig_multi, use_container_width=True)
            st.info("Le score de fragilité est calculé par une combinaison linéaire de plusieurs facteurs de risque.")

    else:
        st.warning("Ajoutez au moins 3 patients pour activer les modèles statistiques.")s
