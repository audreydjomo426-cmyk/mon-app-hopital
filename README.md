# mon-app-hopital
# HospitData - Système de Collecte & Analyse Médicale

**HospitData** est une application web innovante conçue pour la collecte et la visualisation en temps réel des constantes vitales des patients en milieu hospitalier. Ce projet répond aux exigences de robustesse, d'efficacité et de créativité dans le secteur de la santé.

## Lien de l'application
[Accéder à l'application en ligne](https://collecte-hopital-djomo-audrey.streamlit.app/)

---

## Caractéristiques de Qualité

### Créativité & Imagination
L'application ne se contente pas de stocker des chiffres. Elle transforme les données médicales en **indicateurs visuels interactifs**. Le choix du secteur hospitalier a permis de concevoir une interface adaptée aux besoins critiques des soignants (code couleur pour les alertes de température, suivi de la douleur).

###  Robustesse
Le système intègre des mécanismes de contrôle de saisie pour garantir l'intégrité des données :
- **Validation des plages :** Empêche la saisie de températures ou de fréquences cardiaques physiologiquement impossibles.
- **Gestion des erreurs :** Détection automatique des champs obligatoires manquants.
- **Architecture Cloud :** Déploiement stable via Streamlit Cloud avec gestion automatisée des dépendances.

### Efficacité
- **Temps Réel :** Les graphiques se mettent à jour instantanément après chaque soumission de formulaire.
- **Dashboard Analytique :** Centralisation des données pour une lecture rapide par le médecin-chef.
- **Exportation :** Possibilité d'extraire les données pour une utilisation externe (Format CSV).

---

##  Technologies utilisées
* **Langage :** Python 3.8.10
* **Framework Web :** Streamlit
* **Analyse de données :** Pandas
* **Visualisation :** Plotly Express
* **Déploiement :** GitHub & Streamlit Cloud

---

## Installation locale
Si vous souhaitez tester l'application sur votre propre machine :

1. Clonez le dépôt :
   ```bash
   git clone [https://github.com/VOTRE_PSEUDO/mon-app-hopital.git](https://github.com/VOTRE_PSEUDO/mon-app-hopital.git)
