# ChatTelegram Bot

## Description
Ce projet implémente un bot Telegram nommé Aïa, un assistant personnel numérique. Le bot est conçu pour interagir avec les utilisateurs en français, répondre à leurs questions, et les aider dans leurs projets techniques, professionnels et créatifs. Il utilise l'API Groq pour générer des réponses basées sur le modèle Llama.

## Fonctionnalités
- Commande `/start` : Démarre une conversation avec le bot.
- Commande `/reset` : Réinitialise la mémoire du bot pour recommencer une conversation à zéro.
- Gestion de l'historique des conversations avec une limite de 40 échanges.
- Réponses générées par le modèle Llama via l'API Groq.

## Prérequis
- Python 3.10 ou supérieur
- Un compte Telegram avec un bot configuré (obtenez le token via BotFather).
- Une clé API Groq.
- Un fichier `.env` contenant les variables suivantes :
  ```env
  BOT_TOKEN=<votre_token_telegram>
  GROQ_API_KEY=<votre_clé_api_groq>
  ```

## Installation
1. Clonez ce dépôt :
   ```bash
   git clone <url_du_dépôt>
   cd ChatTelegram
   ```
2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Configuration
1. Créez un fichier `.env` à la racine du projet et ajoutez vos clés :
   ```env
   BOT_TOKEN=<votre_token_telegram>
   GROQ_API_KEY=<votre_clé_api_groq>
   ```
2. Assurez-vous que le fichier `histories.json` existe à la racine du projet. Si ce n'est pas le cas, il sera créé automatiquement.

## Déploiement sur Render
1. Connectez-vous à [Render](https://render.com).
2. Créez un nouveau service web et connectez ce dépôt.
3. Configurez les variables d'environnement dans Render :
   - `BOT_TOKEN`
   - `GROQ_API_KEY`
4. Définissez la commande de démarrage :
   ```bash
   python main.py
   ```

## Utilisation
- Démarrez le bot en exécutant le script `main.py` :
  ```bash
  python main.py
  ```
- Interagissez avec le bot via Telegram.

## Structure du projet
- `main.py` : Contient la logique principale du bot Telegram.
- `utils.py` : Fournit des fonctions utilitaires pour gérer l'historique et interagir avec l'API Groq.
- `histories.json` : Fichier JSON pour stocker l'historique des conversations.

## Remarques
- Le bot est conçu pour répondre uniquement en français.
- L'historique des conversations est limité à 40 échanges pour éviter une surcharge.

## Auteur
Martial AVADRA

## Licence
Ce projet est sous licence MIT.