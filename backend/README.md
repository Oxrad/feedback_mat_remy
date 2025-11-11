<!-- aller dans /backend -->
<!-- creer si ce n'es pas déja fait le venv : python3 -m venv backend-venv -->
<!-- activer venv : macos source venv/bin/activate / windows : venv\Scripts\activate -->
<!-- installer fastapi : pip install "fastapi[standard]"         -->
<!-- lancer le serveur fastapi dev main.py -->
# Backend (FastAPI)

Petit README pour démarrer le serveur FastAPI du dossier `backend`.

## Pré-requis
- Python 3.8+
- Git (optionnel)
- Accès terminal / PowerShell

## Installation et activation de l'environnement virtuel
Depuis le dossier `/backend` :

macOS / Linux
```bash
python3 -m venv backend-venv
source backend-venv/bin/activate
```

Windows (PowerShell)
```powershell
python -m venv backend-venv
.\backend-venv\Scripts\activate
```

## Installer les dépendances
```bash
pip install -r requirements.txt
```

Pour figer les dépendances :
```bash
pip freeze > requirements.txt
```

## Lancer le serveur en mode développement
Depuis le dossier où se trouve `main.py` en mode dev :
```bash
fastapi dev main.py
```
