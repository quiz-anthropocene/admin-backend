# Know Your Planet 🌍

Mieux apréhender les limites de notre planète, à travers des questions simples et sourcées.

## But

- Rassembler un ensemble de connaissances sous forme de questions (QCM uniquement pour l'instant)
- Couvrir un large panel de sujets: climat, biodiversité, énergie, consommation, ...
- Des questions avec différents niveaux de difficultés, pour sensibiliser ou se perfectionner
- Une rigueur scientifique dans le choix des questions, et surtout dans les explications apportées autour de la réponse
- Une base de donnée facilement accessible et editable
- Une application simple pour une prise en main rapide

## Infos supplémentaires

- Les questions sont stockées au format YAML, dans le fichier `api/questions/questions.yaml`
- Le code et les questions sont en open-source: venez nous aider !

## Tech

- Une API en Python (Django)
- Une base de donnée SQLite (à faire évoluer)
- Un fichier YAML qui regroupe toutes les questions (facilement editable au sein de Github)
- Une console Admin (Django)

## Lancer le projet en local

### Installer l'application

- Vous devez avoir Python 3.7 installé sur votre machine
- Clonez le code en local
    ```
    git clone git@github.com:raphodn/know-your-planet.git
    ```
- Installez les dépendances du Backend
    ```
    pip install -r requirements.txt
    ```
- Lancez les migrations
    ```
    python manage.py migrate
    ```
- Chargez la base de donnée
    ```
    python manage.py loaddata api/questions/questions.yaml
    ```
- Installez les dépendances du Frontend
    ```
    cd frontend
    yarn install
    ```

### Lancer l'application

#### Lancer le Backend

```
python manage.py runserver
```

Le Backend sera accessible à l'url `http://localhost:8000`

#### Lancer le Frontend

```
cd frontend
yarn serve
```

Le Frontend sera accessible à l'url `http://localhost:8080`

### Accéder à la console admin

Créez d'abord un utilisateur admin
```
python manage.py createsuperuser --username admin@email.com
```

Connectez-vous ensuite sur `http://localhost:8000/admin`

### Autres commandes utiles

Exporter les questions de la base au format YAML
```
python manage.py dumpdata api.question --format=yaml --pretty > api/questions/questions.yaml
```

## Qui sommes-nous ?

A venir

## Idées

- Rajouter un bouton "Autre question dans la même catégorie"
- Proposer à l'utilisateur un feedback rapide sur la question (👍, 👎, voire 💬)
- Rajouter de nouveaux formats de questions: Vrai/Faux par exemple
- Pouvoir mettre des images (ou plutôt des liens vers des images) dans la partie explication ou liens (ou un nouveau champs image ?)
- Remise à plat des catégories au profit de tags ? (une question pourrait appartenir à plusieurs catégories)