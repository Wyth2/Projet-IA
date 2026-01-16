# Agent Intelligent Sémantique et Génératif - Projet de Recommandations de Films

## 📋 Description du Projet

Ce projet implémente un **Agent Intelligent Sémantique et Génératif** utilisant les technologies de RAG (Retrieval Augmented Generation) pour fournir des recommandations de films personnalisées et contextuelles.

### Caractéristiques Principales

- **Système RAG complet** avec base vectorielle ChromaDB
- **Agent conversationnel** avec mémoire de contexte
- **API REST** avec FastAPI
- **Interface utilisateur** interactive avec Streamlit
- **Recherche sémantique** basée sur les embeddings OpenAI
- **Génération contextuelle** avec GPT-3.5-turbo

## 🏗️ Architecture du Système

```
┌─────────────────────┐
│   Interface Web     │  (Streamlit)
│   (app.py)          │
└──────────┬──────────┘
           │ HTTP
           ▼
┌─────────────────────┐
│   API REST          │  (FastAPI)
│   (api.py)          │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Système RAG       │  (LangChain)
│   (rag_system.py)   │
└──────────┬──────────┘
           │
     ┌─────┴─────┐
     ▼           ▼
┌─────────┐ ┌─────────┐
│ChromaDB │ │ OpenAI  │
│Embeddings│ │GPT-3.5  │
└─────────┘ └─────────┘
```

## 📂 Structure du Projet

```
Projet DATA IA/
├── .github/
│   └── copilot-instructions.md    # Instructions pour Copilot
├── src/
│   ├── __init__.py                # Package marker
│   ├── data_processor.py          # Traitement des données
│   └── rag_system.py              # Système RAG principal
├── tests/
│   ├── __init__.py                # Package marker
│   └── test_rag_system.py         # Tests unitaires
├── data/
│   └── chroma_db/                 # Base vectorielle (généré)
├── api.py                         # Backend FastAPI
├── app.py                         # Interface Streamlit
├── config.py                      # Configuration
├── init_db.py                     # Script d'initialisation
├── requirements.txt               # Dépendances
├── .env                           # Configuration locale
├── .env.example                   # Template de configuration
├── .gitignore                     # Fichiers à ignorer
├── README.md                      # Documentation principale
├── QUICKSTART.md                  # Guide rapide
└── venv/                          # Environnement virtuel
```

## 🚀 Installation et Configuration

### Prérequis

- Python 3.10 ou supérieur
- Clé API OpenAI
- 2 GB d'espace disque libre

### Installation

1. **Environnement virtuel** (déjà créé)
```bash
venv\Scripts\activate
```

2. **Dépendances** (déjà installées)
```bash
pip install -r requirements.txt
```

3. **Configuration**
Modifiez le fichier `.env` et ajoutez votre clé API OpenAI :
```env
OPENAI_API_KEY=sk-votre_clé_ici
```

4. **Initialisation de la base vectorielle**
```bash
python init_db.py
```

## 🎯 Utilisation

### Lancement du Système

**Terminal 1 - Backend API :**
```bash
python api.py
```
L'API sera disponible sur `http://localhost:8000`

**Terminal 2 - Interface Utilisateur :**
```bash
streamlit run app.py
```
L'interface sera disponible sur `http://localhost:8501`

### Utilisation de l'Interface Web

1. Ouvrez votre navigateur sur `http://localhost:8501`
2. Vérifiez que l'API est connectée (bouton "Vérifier l'API")
3. **Onglet Chat** : Conversez avec l'agent
   - "Recommande-moi des films de science-fiction"
   - "Quels films ressemblent à Inception?"
   - "Je cherche un film d'action avec Leonardo DiCaprio"
4. **Onglet Recherche** : Recherche sémantique directe

### Utilisation de l'API

**Documentation Interactive :** `http://localhost:8000/docs`

**Exemples cURL :**

```bash
# Chat
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Recommande-moi des films de science-fiction\"}"

# Recherche
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"films d action\", \"k\": 5}"

# Réinitialiser la conversation
curl -X POST "http://localhost:8000/reset"
```

## 🧪 Tests

```bash
python -m pytest tests/
```

## 📊 Jeu de Données

Le système inclut 12 films populaires :
- The Shawshank Redemption (1994)
- The Godfather (1972)
- The Dark Knight (2008)
- Pulp Fiction (1994)
- Forrest Gump (1994)
- Inception (2010)
- The Matrix (1999)
- Interstellar (2014)
- Parasite (2019)
- The Prestige (2006)
- Gladiator (2000)
- The Departed (2006)

### Ajouter Plus de Films

Modifiez la méthode `load_sample_movies()` dans [src/data_processor.py](src/data_processor.py):

```python
{
    "id": 13,
    "title": "Votre Film",
    "year": 2024,
    "genre": ["Genre"],
    "director": "Réalisateur",
    "description": "Description du film...",
    "rating": 8.0,
    "actors": ["Acteur 1", "Acteur 2"]
}
```

Puis réinitialisez : `python init_db.py`

## ⚙️ Configuration Avancée

### Paramètres du Modèle ([config.py](config.py))

```python
# Modèles OpenAI
embedding_model = "text-embedding-ada-002"
chat_model = "gpt-3.5-turbo"

# Paramètres de génération
temperature = 0.7          # Créativité (0-1)
max_tokens = 500           # Longueur maximale

# Paramètres RAG
top_k_results = 5          # Nombre de documents récupérés
chunk_size = 1000          # Taille des chunks
chunk_overlap = 200        # Chevauchement
```

### Personnalisation du Prompt

Modifiez le template dans [src/rag_system.py](src/rag_system.py) (ligne ~80) :

```python
template = """Tu es un assistant intelligent spécialisé...
[Votre prompt personnalisé ici]
"""
```

## 🔍 Endpoints API Détaillés

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/` | GET | Information sur l'API |
| `/health` | GET | Vérification de l'état |
| `/chat` | POST | Conversation avec l'agent |
| `/search` | POST | Recherche sémantique |
| `/reset` | POST | Réinitialiser la conversation |
| `/initialize` | POST | Réinitialiser la base vectorielle |

## 🐛 Dépannage

### Problème : Module non trouvé
**Solution :**
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### Problème : Clé OpenAI invalide
**Solution :**
- Vérifiez que `.env` contient une clé valide
- Format : `OPENAI_API_KEY=sk-...`

### Problème : Port déjà utilisé
**Solution :**
Modifiez dans `.env`:
```env
API_PORT=8001
```

### Problème : Erreur ChromaDB
**Solution :**
```bash
# Supprimer la base et réinitialiser
rmdir /s data\chroma_db
python init_db.py
```

## 📚 Technologies Utilisées

- **LangChain** 0.1.0 - Orchestration RAG
- **OpenAI** 1.6.1 - Embeddings et génération
- **ChromaDB** 0.4.22 - Base vectorielle
- **FastAPI** 0.108.0 - API REST
- **Streamlit** 1.29.0 - Interface web
- **Pydantic** 2.5.0 - Validation de données
- **Pandas** 2.1.4 - Manipulation de données

## 📖 Documentation Complémentaire

- [QUICKSTART.md](QUICKSTART.md) - Guide de démarrage rapide
- [.github/copilot-instructions.md](.github/copilot-instructions.md) - Instructions Copilot
- API Docs : `http://localhost:8000/docs`

## 🎓 Contexte Pédagogique

### Objectifs d'Apprentissage

1. **Comprendre le RAG** : Retrieval Augmented Generation
2. **Maîtriser les embeddings** : Représentation vectorielle
3. **Développer un agent** : Système conversationnel
4. **Architecture full-stack** : API + Frontend

### Concepts Clés Implémentés

- ✅ Embeddings vectoriels (OpenAI)
- ✅ Recherche de similarité (ChromaDB)
- ✅ Génération contextuelle (GPT-3.5)
- ✅ Mémoire conversationnelle (LangChain)
- ✅ API REST (FastAPI)
- ✅ Interface interactive (Streamlit)

## 🔒 Sécurité

- **Clés API** : Stockées dans `.env` (non versionné)
- **Variables d'environnement** : Isolation de la configuration
- **CORS** : Configuré dans l'API
- ⚠️ **Production** : Ajouter authentification et rate limiting

## 📈 Évolutions Possibles

- [ ] Ajouter plus de films (base TMDB, IMDb)
- [ ] Support multilingue
- [ ] Filtres avancés (année, genre, acteur)
- [ ] Système de notation utilisateur
- [ ] Recommandations collaboratives
- [ ] Déploiement cloud (AWS, Azure, GCP)
- [ ] Authentification utilisateur
- [ ] Historique des conversations

## 🤝 Contribution

Ce projet est à des fins éducatives. Pour des améliorations :
1. Fork le projet
2. Créez une branche (`git checkout -b feature/amelioration`)
3. Committez (`git commit -m 'Ajout fonctionnalité'`)
4. Push (`git push origin feature/amelioration`)
5. Ouvrez une Pull Request

## 📄 Licence

Projet éducatif - Janvier 2026

## ✉️ Contact

Projet DATA IA - 2026

---

**🎬 Bon visionnage avec votre agent de recommandations !**
