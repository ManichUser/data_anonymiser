#!/bin/bash
echo "🚀 Démarrage de l'application d'anonymisation..."
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null
python app.py
