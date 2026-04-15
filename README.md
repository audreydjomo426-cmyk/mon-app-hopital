## HospitData - Système de Gestion Clinique

HospitData est une solution de santé numérique (e-Health) avancée conçue pour transformer la saisie de données médicales papier en un tableau de bord analytique intelligent. L'application permet une surveillance proactive des patients grâce à un algorithme de triage en temps réel.
 
 Lien de l'application
 
 https://collecte-hopital-djomo-audrey.streamlit.app
 
 Caractéristiques de Qualité (Critères du Devoir)
 Créativité & Imagination

L'application va au-delà d'un simple formulaire. Elle simule un Dossier Médical Partagé (DMP) complet :

    Profil Morphologique : Intégration de l'âge, de la taille et du poids.

    Sécurité Patient : Gestion des groupes sanguins, des allergies et des maladies chroniques (Diabète, Hypertension, etc.).

    Visualisation Multi-dimensionnelle : Utilisation de graphiques croisant l'IMC, le risque clinique et la douleur.

## Robustesse & Intelligence

Le système possède une couche de traitement logique (Backend) qui sécurise la donnée :

    Calculateur d'IMC automatique : Évite les erreurs de calcul manuel.

    Algorithme de Triage (Score de Risque) : Analyse automatique des constantes pour classer les patients (🟢 Stable, 🟠 À surveiller, 🔴 Critique).

    Données de Démonstration : L'application est livrée avec 10 dossiers patients pré-enregistrés pour une analyse immédiate dès le lancement.

## Efficacité & Expérience Utilisateur (UX)

    Interface par Onglets : Séparation claire entre la "Saisie" (Infirmier) et "l'Analyse" (Médecin).

    Interactivité Totale : Les graphiques Plotly permettent de zoomer sur un patient spécifique.

    Portabilité des données : Exportation instantanée en format CSV pour une utilisation sur Excel ou logiciels tiers.
## Technologies utilisées

    Langage : Python 3.x

    Framework Web : Streamlit (Interface réactive)

    Analyse de données : Pandas (Moteur de calcul)

    Visualisation : Plotly Express (Graphiques dynamiques)

    Déploiement : GitHub & Streamlit Cloud

 Installation locale

Pour exécuter ce projet localement :

    Cloner le projet :
    Bash

git clone https://github.com/VOTRE_PSEUDO/mon-app-hopital.git

Installer les dépendances :
Bash

pip install -r requirements.txt

Lancer l'application :
Bash

streamlit run app.py
