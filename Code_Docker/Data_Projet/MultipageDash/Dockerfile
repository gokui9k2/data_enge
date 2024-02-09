# Utiliser l'image de base officielle Python 3
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier des dépendances
COPY requirements.txt /app/

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier les fichiers de l'application dans le conteneur
COPY . /app

# Exposer le port sur lequel Dash s'exécute
EXPOSE 8050


