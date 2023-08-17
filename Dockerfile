# Utilisez une image de base Python
FROM python:3.8-slim

# Créez un répertoire pour votre application
WORKDIR /app

# Copiez les fichiers nécessaires pour l'installation
COPY requirements.txt ./
# Si vous avez d'autres fichiers/dossiers nécessaires, ajoutez-les ici

# Installez les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copiez le reste de votre application
COPY . .

# Définissez la variable d'environnement pour informer Flask qu'il doit s'exécuter en mode production
ENV FLASK_ENV=production

# Exposez le port que votre app va utiliser
EXPOSE 8080

# Lancez votre application
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
