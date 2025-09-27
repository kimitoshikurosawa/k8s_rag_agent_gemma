# --- Étape 1: Définir l'image de base ---
# Nous partons d'une image Python 3.10 optimisée (slim) pour garder une taille raisonnable.
FROM python:3.10-slim

# --- Étape 2: Définir l'environnement de travail ---
# Crée un dossier /code à l'intérieur du conteneur et s'y place.
WORKDIR /code

# --- Étape 3: Installer les dépendances ---
# Copier UNIQUEMENT le fichier des dépendances pour profiter du cache Docker.
# Docker ne réinstallera pas les dépendances si ce fichier ne change pas.
COPY ./app/requirements.txt /code/requirements.txt

# Installer les dépendances.
# --no-cache-dir pour ne pas conserver le cache de pip et alléger l'image.
# --upgrade pip pour s'assurer d'avoir la dernière version de pip.
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt

# --- Étape 4: Copier le reste de l'application ---
# Copier le code de l'application et la base de données vectorielle.
COPY ./app /code/app

# --- Étape 5: Exposer le port ---
# Indiquer que l'application à l'intérieur du conteneur écoutera sur le port 8000.
EXPOSE 8000

# --- Étape 6: Définir la commande de démarrage ---
# La commande à exécuter lorsque le conteneur démarre.
# "uvicorn" est le serveur qui fait tourner notre application FastAPI.
# "host 0.0.0.0" est crucial pour rendre l'application accessible depuis l'extérieur du conteneur.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]