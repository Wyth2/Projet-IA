# 📝 Aide-Mémoire - Commandes Essentielles

## 🚀 Commandes de Démarrage

### Activer l'environnement virtuel
```bash
# Windows PowerShell
venv\Scripts\activate

# Vous verrez (venv) apparaître devant votre prompt
```

### Lancer l'API (Backend)
```bash
python api.py

# Résultat attendu :
# INFO: Uvicorn running on http://0.0.0.0:8000
# RAG system ready!
```

### Lancer l'Interface (Frontend)
```bash
streamlit run app.py

# Résultat attendu :
# Local URL: http://localhost:8501
# Le navigateur s'ouvre automatiquement
```

### Initialiser/Réinitialiser la Base de Données
```bash
python init_db.py

# Résultat attendu :
# ✅ Initialisation terminée avec succès!
```

---

## 🔧 Commandes d'Installation

### Installer les dépendances
```bash
pip install -r requirements.txt
```

### Mettre à jour pip
```bash
python -m pip install --upgrade pip
```

### Créer l'environnement virtuel (si besoin)
```bash
py -m venv venv
```

---

## 🧪 Commandes de Test

### Lancer tous les tests
```bash
python -m pytest tests/
```

### Lancer un test spécifique
```bash
python -m pytest tests/test_rag_system.py
```

### Tests avec détails
```bash
python -m pytest tests/ -v
```

---

## 🌐 URLs Importantes

```
Interface Utilisateur : http://localhost:8501
API Backend          : http://localhost:8000
Documentation API    : http://localhost:8000/docs
API Health Check     : http://localhost:8000/health
```

---

## 📦 Commandes Git (si versioning)

### Initialiser le repo
```bash
git init
git add .
git commit -m "Initial commit: Agent RAG pour recommandations films"
```

### Ajouter des changements
```bash
git add .
git commit -m "Description des changements"
git push origin main
```

---

## 🔍 Commandes de Débogage

### Vérifier la version de Python
```bash
python --version
# Attendu : Python 3.10 ou supérieur
```

### Lister les packages installés
```bash
pip list
```

### Vérifier si un port est utilisé
```bash
# Windows PowerShell
netstat -ano | findstr :8000  # Pour l'API
netstat -ano | findstr :8501  # Pour Streamlit
```

### Tuer un processus sur un port
```bash
# Windows PowerShell
# Trouvez le PID avec netstat puis :
taskkill /PID <numero_pid> /F
```

---

## 📝 Commandes de Gestion de Fichiers

### Voir la structure du projet
```bash
tree /F
```

### Créer une sauvegarde
```bash
# Copier tout le dossier (hors venv)
robocopy "Projet DATA IA" "Backup Projet DATA IA" /E /XD venv
```

### Nettoyer les fichiers Python compilés
```bash
# PowerShell
Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item
Get-ChildItem -Recurse -Filter "__pycache__" | Remove-Item -Recurse
```

---

## 🗑️ Commandes de Nettoyage

### Réinitialiser complètement la base ChromaDB
```bash
rmdir /s /q data\chroma_db
python init_db.py
```

### Réinstaller toutes les dépendances
```bash
pip freeze > requirements_old.txt
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### Recréer l'environnement virtuel
```bash
rmdir /s /q venv
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## 📊 Commandes de Monitoring

### Voir les logs de l'API en temps réel
```bash
# L'API affiche déjà les logs dans le terminal
# Pour sauvegarder dans un fichier :
python api.py > api_logs.txt 2>&1
```

### Voir l'utilisation mémoire
```bash
# Windows PowerShell
Get-Process python | Select-Object ProcessName, @{Name="Memory(MB)";Expression={$_.WorkingSet64 / 1MB}}
```

---

## 🔑 Variables d'Environnement

### Afficher les variables actuelles (sans exposer les secrets)
```bash
# Vérifier que OPENAI_API_KEY est définie
echo $env:OPENAI_API_KEY
# Ne devrait rien afficher (normal, elle est dans .env)
```

### Définir temporairement (pour test)
```bash
$env:OPENAI_API_KEY = "sk-test-..."
python init_db.py
```

---

## 🆘 Commandes d'Urgence

### Arrêter tous les processus Python
```bash
# Windows PowerShell (ATTENTION : ferme tous les Python!)
Get-Process python | Stop-Process -Force
```

### Vérifier que tout est bien arrêté
```bash
Get-Process python
# Devrait retourner : "Get-Process : Cannot find a process..."
```

### Redémarrer proprement
```bash
# Terminal 1
venv\Scripts\activate
python api.py

# Terminal 2 (nouveau)
venv\Scripts\activate
streamlit run app.py
```

---

## 📚 Commandes de Documentation

### Générer la documentation des modules (si Sphinx installé)
```bash
pip install sphinx
sphinx-quickstart docs
sphinx-apidoc -o docs/source src/
```

### Voir l'aide d'un script
```bash
python api.py --help
python init_db.py --help
```

---

## 🔄 Workflow Typique de Développement

```bash
# 1. Activer l'environnement
venv\Scripts\activate

# 2. Faire des modifications dans le code
# ... éditer les fichiers ...

# 3. Tester
python -m pytest tests/

# 4. Réinitialiser la DB si besoin
python init_db.py

# 5. Lancer l'API
python api.py

# 6. Dans un autre terminal, lancer l'interface
venv\Scripts\activate
streamlit run app.py

# 7. Tester dans le navigateur
# http://localhost:8501
```

---

## 💾 Sauvegardes Rapides

### Sauvegarder la configuration
```bash
copy .env .env.backup
copy config.py config.py.backup
```

### Sauvegarder les données
```bash
robocopy data data_backup /E
```

---

## 📞 Contacts et Ressources

### Documentation Locale
- [README.md](README.md) - Documentation complète
- [QUICKSTART.md](QUICKSTART.md) - Démarrage rapide
- [GUIDE_VISUEL.md](GUIDE_VISUEL.md) - Guide visuel
- [PROJET_COMPLETE.md](PROJET_COMPLETE.md) - Récapitulatif

### Documentation Externe
- LangChain : https://python.langchain.com/docs/
- OpenAI API : https://platform.openai.com/docs
- ChromaDB : https://docs.trychroma.com/
- FastAPI : https://fastapi.tiangolo.com/
- Streamlit : https://docs.streamlit.io/

---

## 🎯 Raccourcis Clavier Utiles

### Dans VS Code / PowerShell
```
Ctrl + C          : Arrêter un processus
Ctrl + Shift + `  : Nouveau terminal
Ctrl + `          : Afficher/masquer terminal
Ctrl + K, Ctrl + 0: Tout fermer dans l'éditeur
Ctrl + P          : Recherche rapide de fichier
```

### Dans le navigateur (Streamlit)
```
R                 : Recharger l'application
C                 : Effacer le cache
```

---

## 📋 Checklist Quotidienne

```
☐ Environnement virtuel activé
☐ .env configuré avec clé OpenAI valide
☐ Base de données initialisée
☐ API lancée (Terminal 1)
☐ Interface lancée (Terminal 2)
☐ Navigateur ouvert sur localhost:8501
☐ Test de connexion API réussi
```

---

## 🎉 Vous Êtes Prêt !

Gardez ce fichier sous la main pour référence rapide.

**Astuce** : Créez un raccourci Windows vers `venv\Scripts\activate.ps1` 
pour activer l'environnement rapidement !
