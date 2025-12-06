# 🔒 Application d'Anonymisation de Données

Application web Flask pour anonymiser vos données sensibles de manière sécurisée et intuitive.

## �� Fonctionnalités

- ✅ Upload de fichiers multiples (CSV, Excel)
- ✅ Sélection interactive des colonnes à anonymiser
- ✅ Anonymisation SHA-256 (irréversible)
- ✅ Jointure automatique des données
- ✅ Prévisualisation des résultats
- ✅ Téléchargement des fichiers anonymisés
- ✅ Interface responsive et moderne

## 📦 Installation

### 1. Créer un environnement virtuel

```bash
python3 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Lancer l'application

```bash
python app.py
```

L'application sera accessible sur : http://localhost:5000

## 📖 Utilisation

1. **Choisissez le nombre de fichiers** à anonymiser (1-10)
2. **Téléversez vos fichiers** (CSV, XLSX, XLS)
3. **Sélectionnez les colonnes** contenant des données sensibles
4. **Choisissez la colonne de jointure** commune
5. **Lancez l'anonymisation** et visualisez les résultats
6. **Téléchargez** vos fichiers anonymisés

## 🏗️ Structure du Projet

```
data-anonymizer/
├── app.py                  # Application principale Flask
├── requirements.txt        # Dépendances Python
├── services/              # Logique métier
│   ├── __init__.py
│   ├── anonymization_service.py
│   ├── file_service.py
│   └── merge_service.py
├── templates/             # Templates HTML
│   └── index.html
├── static/                # Fichiers statiques
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── uploads/               # Dossier de téléversement
├── test.py                # cree deux fichiers xls dans mock
└── docs/                  # Documentation

```

## 🔐 Sécurité

- Anonymisation SHA-256 (irréversible)
- Limite de taille : 16 MB par fichier
- Validation des formats de fichiers
- Stockage temporaire en mémoire

## 🛠️ Technologies

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Data Processing**: Pandas
- **File Handling**: openpyxl

## 👨‍💻 Auteur
Mani-X
# data_anonymiser
