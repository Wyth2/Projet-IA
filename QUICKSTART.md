# Guide de Démarrage Rapide

## Installation en 5 Minutes

### 1. Créer l'environnement virtuel
```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Configurer la clé API
- Copiez `.env.example` vers `.env`
- Ajoutez votre clé OpenAI dans `.env`

### 4. Initialiser la base de données
```bash
python init_db.py
```

### 5. Lancer l'application

**Terminal 1 - API:**
```bash
python api.py
```

**Terminal 2 - Interface:**
```bash
streamlit run app.py
```

## Accès

- **Interface Web**: http://localhost:8501
- **API**: http://localhost:8000
- **Documentation API**: http://localhost:8000/docs

## Premiers Tests

### Via l'Interface
1. Ouvrez http://localhost:8501
2. Cliquez sur "Vérifier l'API"
3. Tapez: "Recommande-moi des films de science-fiction"

### Via l'API
```bash
curl -X POST "http://localhost:8000/chat" -H "Content-Type: application/json" -d "{\"message\": \"Recommande-moi des films de science-fiction\"}"
```

## Problèmes Courants

### "Module not found"
```bash
pip install -r requirements.txt
```

### "OpenAI API key not configured"
Vérifiez que votre fichier `.env` contient:
```
OPENAI_API_KEY=sk-...
```

### "Port already in use"
Modifiez les ports dans `.env`:
```
API_PORT=8001
```
