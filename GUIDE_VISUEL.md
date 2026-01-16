# 🎬 Guide de Démarrage Visuel

## 🚀 Démarrage en 3 Minutes

### ⚙️ Configuration Initiale (1 fois seulement)

#### 1. Ouvrir le fichier `.env`
```
Projet DATA IA/
└── .env  ← Double-cliquez pour ouvrir
```

#### 2. Ajouter votre clé OpenAI
```env
# Avant (à remplacer) :
OPENAI_API_KEY=your_openai_api_key_here

# Après (votre vraie clé) :
OPENAI_API_KEY=sk-proj-...votre_clé_ici...
```

💡 **Obtenir une clé** : https://platform.openai.com/api-keys

#### 3. Initialiser la base de données

Ouvrez un terminal dans le dossier du projet :

```bash
# Windows PowerShell
venv\Scripts\activate
python init_db.py
```

Vous devriez voir :
```
==================================================
Initialisation de la Base de Données Vectorielle
==================================================

✓ Clé API OpenAI: sk-proj-12...
✓ Répertoire de persistance: ./data/chroma_db

📚 Initialisation du système RAG...
🔄 Chargement et indexation des films...
Vector store initialized with 12 documents

✅ Initialisation terminée avec succès!
```

---

## 🎯 Utilisation Quotidienne

### Étape 1 : Lancer l'API

**Terminal 1 :**
```bash
venv\Scripts\activate
python api.py
```

✅ **Résultat attendu :**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
Initializing RAG system...
RAG system ready!
```

⚠️ **Laissez ce terminal ouvert !**

---

### Étape 2 : Lancer l'Interface

**Terminal 2 (nouveau) :**
```bash
venv\Scripts\activate
streamlit run app.py
```

✅ **Résultat attendu :**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

🌐 **Votre navigateur s'ouvre automatiquement !**

---

## 🎮 Interface Utilisateur

### Vue d'Ensemble

```
┌─────────────────────────────────────────────────────┐
│ 🎬 CinéMind - Votre conseiller cinéma intelligent   │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ⚙️ Configuration          ℹ️ À propos            │
│  ┌──────────────┐          Agent utilisant:        │
│  │ 🔄 Vérifier  │          • RAG                    │
│  │   l'API      │          • OpenAI                 │
│  └──────────────┘          • ChromaDB               │
│                            • LangChain              │
│  ✅ API connectée                                   │
│                                                     │
│  ────────────────                                   │
│                                                     │
│  🗑️ Réinitialiser                                  │
│     la conversation                                 │
│                                                     │
├─────────────────────────────────────────────────────┤
│  [💬 Chat]  [🔍 Recherche]                         │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Conversation avec l'Agent                          │
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │ 👤 Vous:                                    │   │
│  │ Recommande-moi des films de science-fiction│   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │ 🤖 Assistant:                               │   │
│  │ Je vous recommande "Inception" (2010)...    │   │
│  │                                             │   │
│  │ 📚 Sources utilisées ▼                      │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  ────────────────                                   │
│                                                     │
│  Votre message: ___________________________         │
│  📤 [Envoyer]                                       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 💬 Exemples de Questions

### Questions Générales
```
❓ "Recommande-moi des films de science-fiction"
❓ "Je cherche un bon thriller"
❓ "Quels sont les meilleurs films d'action ?"
```

### Questions Spécifiques
```
❓ "Quels films ressemblent à Inception ?"
❓ "Je cherche un film avec Leonardo DiCaprio"
❓ "Parle-moi de The Matrix"
```

### Questions Détaillées
```
❓ "Je veux un film dramatique des années 90 avec une note élevée"
❓ "Recommande-moi un film de Christopher Nolan"
❓ "Quel film regarder si j'ai aimé The Shawshank Redemption ?"
```

---

## 🔍 Onglet Recherche

```
┌─────────────────────────────────────────────────────┐
│  [💬 Chat]  [🔍 Recherche]                         │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Recherche Sémantique de Films                      │
│  Effectuez une recherche sémantique dans la base    │
│                                                     │
│  Votre recherche:                                   │
│  ┌─────────────────────────────────────────────┐   │
│  │ films d'action avec effets spéciaux        │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  Nombre de résultats: [●─────] 5                   │
│                                                     │
│  🔍 [Rechercher]                                    │
│                                                     │
│  ✅ 5 résultats trouvés                             │
│                                                     │
│  ▶ 🎬 Résultat 1                                   │
│  ▶ 🎬 Résultat 2                                   │
│  ▶ 🎬 Résultat 3                                   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 📊 Tableau de Bord Terminal

### Terminal 1 - API (Backend)

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
Initializing RAG system...
Vector store loaded successfully
Conversation chain ready
RAG system ready!
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000

INFO:     127.0.0.1:52341 - "POST /chat HTTP/1.1" 200 OK
INFO:     127.0.0.1:52342 - "GET /health HTTP/1.1" 200 OK
```

### Terminal 2 - Interface (Frontend)

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.100:8501

[status] Running Streamlit v1.29.0
```

---

## 🔄 Cycle de Fonctionnement

```
┌─────────────┐
│  Utilisateur│
│   (vous)    │
└──────┬──────┘
       │ 1. Question
       ▼
┌─────────────────┐
│   Interface     │
│   Streamlit     │
└──────┬──────────┘
       │ 2. HTTP Request
       ▼
┌─────────────────┐
│   API FastAPI   │
└──────┬──────────┘
       │ 3. Process
       ▼
┌─────────────────┐
│  Système RAG    │
│   (LangChain)   │
└──────┬──────────┘
       │
   ┌───┴───┐
   │       │ 4. Search + Generate
   ▼       ▼
┌─────┐ ┌─────┐
│Chroma│ │OpenAI│
│  DB  │ │ GPT │
└─────┘ └─────┘
   │       │
   └───┬───┘
       │ 5. Response
       ▼
┌─────────────────┐
│   Utilisateur   │
│ (réponse reçue) │
└─────────────────┘
```

---

## 🛠️ Dépannage Visuel

### ❌ Problème : "API non disponible"

**Cause :** L'API n'est pas lancée

**Solution :**
```
Terminal 1:
venv\Scripts\activate
python api.py

Attendez de voir:
✅ "RAG system ready!"
```

---

### ❌ Problème : "OpenAI API key not configured"

**Cause :** Clé API manquante ou invalide

**Solution :**
```
1. Ouvrir .env
2. Vérifier : OPENAI_API_KEY=sk-proj-...
3. Sauvegarder
4. Relancer : python api.py
```

---

### ❌ Problème : "Module not found"

**Cause :** Dépendances non installées

**Solution :**
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

---

## 📈 Progression Typique

```
Jour 1:
├─ ✅ Installation
├─ ✅ Configuration
└─ ✅ Premier test

Jour 2:
├─ ✅ Comprendre le fonctionnement
├─ ✅ Tester différentes questions
└─ ✅ Explorer l'API

Jour 3+:
├─ ✅ Ajouter des films
├─ ✅ Personnaliser le prompt
└─ ✅ Améliorer le système
```

---

## 🎯 Checklist de Démarrage

- [ ] Clé OpenAI configurée dans `.env`
- [ ] Base de données initialisée (`python init_db.py`)
- [ ] API lancée (Terminal 1)
- [ ] Interface lancée (Terminal 2)
- [ ] Navigateur ouvert sur `http://localhost:8501`
- [ ] Bouton "Vérifier l'API" cliqué
- [ ] Première question testée
- [ ] Résultat reçu avec succès !

---

## 🎉 Vous êtes Prêt !

Maintenant que tout est configuré, **explorez et amusez-vous** avec votre agent de recommandations de films ! 🎬

**Astuce :** Gardez les deux terminaux ouverts pendant l'utilisation.

---

💡 **Besoin d'aide ?** Consultez README.md ou QUICKSTART.md
