# 🎬 Agent Intelligent Sémantique et Génératif

## Système de Recommandations de Films avec RAG

> **Projet complet d'IA conversationnelle utilisant Retrieval Augmented Generation (RAG)**  
> Recommandations de films personnalisées • Recherche sémantique • Interface interactive

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.108.0-green)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-red)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1.0-yellow)](https://python.langchain.com/)

---

## ⚡ Démarrage Ultra-Rapide

```bash
# 1. Configurer votre clé OpenAI dans .env
OPENAI_API_KEY=sk-votre_clé_ici

# 2. Initialiser
python init_db.py

# 3. Lancer (2 terminaux)
python api.py              # Terminal 1
streamlit run app.py       # Terminal 2

# 4. Ouvrir → http://localhost:8501
```

**📖 Plus de détails ?** → [START.md](START.md) ou [QUICKSTART.md](QUICKSTART.md)

---

## 🎬 Agent Intelligent Sémantique et Génératif

## Système de Recommandations de Films avec RAG

Ce projet implémente un agent conversationnel intelligent utilisant la technologie RAG (Retrieval Augmented Generation) pour fournir des recommandations de films personnalisées et contextuelles.

## 🚀 Fonctionnalités

- **Recherche Sémantique**: Recherche de films basée sur la similarité sémantique
- **Conversation Contextuelle**: Agent conversationnel avec mémoire
- **Recommandations Intelligentes**: Suggestions basées sur les préférences et le contexte
- **Interface Intuitive**: Interface web moderne avec Streamlit
- **API REST**: Backend FastAPI pour l'intégration

## 📋 Architecture

```
├── src/
│   ├── data_processor.py    # Traitement des données de films
│   └── rag_system.py         # Système RAG avec ChromaDB
├── api.py                    # Backend FastAPI
├── app.py                    # Interface Streamlit
├── config.py                 # Configuration centralisée
├── requirements.txt          # Dépendances Python
├── .env.example              # Template de configuration
└── README.md                 # Ce fichier
```

## 🛠️ Technologies Utilisées

- **LangChain**: Orchestration du système RAG
- **OpenAI**: Embeddings et génération de texte
- **ChromaDB**: Base de données vectorielle
- **FastAPI**: Framework API REST
- **Streamlit**: Interface utilisateur
- **Python 3.10+**: Langage de programmation

## 📦 Installation

### 1. Cloner le projet

```bash
cd "Projet DATA IA"
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configuration

Copiez le fichier `.env.example` en `.env` et ajoutez votre clé API OpenAI:

```bash
copy .env.example .env
```

Modifiez le fichier `.env`:

```env
OPENAI_API_KEY=votre_clé_api_openai_ici
```

## 🚀 Utilisation

### Démarrer le Backend (API)

Dans un premier terminal:

```bash
python api.py
```

L'API sera accessible sur `http://localhost:8000`

### Démarrer l'Interface Utilisateur

Dans un second terminal:

```bash
streamlit run app.py
```

L'interface sera accessible sur `http://localhost:8501`

## 📖 Guide d'Utilisation

### 1. Conversation avec l'Agent

- Ouvrez l'interface Streamlit
- Utilisez l'onglet "💬 Chat"
- Posez des questions comme:
  - "Recommande-moi des films de science-fiction"
  - "Quels films ressemblent à Inception?"
  - "Je cherche un film d'action avec Leonardo DiCaprio"

### 2. Recherche Sémantique

- Utilisez l'onglet "🔍 Recherche"
- Entrez une description ou des mots-clés
- Ajustez le nombre de résultats souhaités
- Explorez les films trouvés

### 3. Utiliser l'API Directement

#### Chat

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Recommande-moi des films de science-fiction"}'
```

#### Recherche

```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "films d action", "k": 5}'
```

## 🎯 Fonctionnement du Système RAG

1. **Indexation**: Les films sont convertis en embeddings vectoriels et stockés dans ChromaDB
2. **Recherche**: Lors d'une question, le système trouve les films les plus similaires
3. **Génération**: GPT-3.5 génère une réponse contextuelle basée sur les films trouvés
4. **Mémoire**: L'historique de conversation est maintenu pour un dialogue cohérent

## 📊 Données

Le système inclut 12 films populaires pour la démonstration:
- The Shawshank Redemption
- The Godfather
- The Dark Knight
- Pulp Fiction
- Forrest Gump
- Inception
- The Matrix
- Interstellar
- Parasite
- The Prestige
- Gladiator
- The Departed

### Ajouter Plus de Films

Modifiez `src/data_processor.py` et ajoutez vos films dans la méthode `load_sample_movies()`.

## 🔧 Configuration Avancée

### Paramètres du Modèle (config.py)

```python
embedding_model = "text-embedding-ada-002"  # Modèle d'embeddings
chat_model = "gpt-3.5-turbo"               # Modèle de chat
temperature = 0.7                           # Créativité (0-1)
max_tokens = 500                            # Longueur maximale
top_k_results = 5                           # Nombre de résultats RAG
```

## 📝 Endpoints API

- `GET /` - Information sur l'API
- `GET /health` - Vérification de l'état
- `POST /chat` - Conversation avec l'agent
- `POST /search` - Recherche sémantique
- `POST /reset` - Réinitialiser la conversation
- `POST /initialize` - Réinitialiser la base vectorielle

## 🐛 Dépannage

### L'API ne démarre pas

- Vérifiez que la clé OpenAI est valide dans `.env`
- Assurez-vous que le port 8000 est disponible

### Erreur avec ChromaDB

- Supprimez le dossier `data/chroma_db/`
- Relancez l'API pour recréer la base

### Erreur d'importation

- Vérifiez l'activation de l'environnement virtuel
- Réinstallez les dépendances: `pip install -r requirements.txt`

## 📚 Ressources

- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Reference](https://platform.openai.com/docs)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)

## 🎓 Projet Académique

Ce projet a été développé dans le cadre du cours d'IA Générative - Agent Intelligent Sémantique et Génératif (2026).

### Objectifs Pédagogiques

- Comprendre et implémenter un système RAG
- Utiliser des embeddings vectoriels pour la recherche sémantique
- Créer un agent conversationnel contextuel
- Développer une application full-stack avec IA

## 📄 Licence

Ce projet est à des fins éducatives.

## 👥 Auteur

Projet DATA IA - 2026

---

**Note**: Assurez-vous d'avoir une clé API OpenAI valide et des crédits disponibles pour utiliser ce projet.
