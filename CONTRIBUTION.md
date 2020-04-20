# Contribuer

Merci d'être là et de vouloir contribuer :)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Comment aider ?](#comment-aider-)
- [Rajouter ou modifier des questions](#rajouter-ou-modifier-des-questions)
- [Proposer des améliorations de l'application](#proposer-des-am%C3%A9liorations-de-lapplication)
- [Aider au développement de l'application](#aider-au-d%C3%A9veloppement-de-lapplication)
- [Informations supplémentaires](#informations-suppl%C3%A9mentaires)
  - [Stack technique](#stack-technique)
  - [Lancer le projet en local](#lancer-le-projet-en-local)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Comment aider ?

Il y a plusieurs aspects du projet qui ont besoin d'aide:

- La base de donnée de questions:
    - rajouter de nouvelles questions
    - proposer des modifications sur des questions existantes
- L'application:
    - Remonter les bugs
    - Faire des propositions d'améliorations (grâce aux Issues Github)
    - Aider à développer l'application (grâce aux Issues et Pull Requests Github)

## Rajouter ou modifier des questions

Toutes les questions de la base de donnée de l'application peuvent être vues dans le fichier `api/data/questions.yaml`

*Mais* ce n'est pas la source de la base de donnée, seulement un export.

Toutes les questions (finalisées ou en cours de création) sont dans actuellement dans un fichier Google Sheet, que l'on synchronise régulièrement avec la base de donnée.

Faites-moi signe si vous voulez avoir accès à ce Google Sheet (libre accès).

## Proposer des améliorations de l'application

Vous avez vu un bug ? Vous trouvez l'app contre-intuitive, ou simplement avez une idée pour rendre le design plus beau/propre ?

Il suffit de créer une Issue dans l'interface Github du projet ([ici](https://github.com/raphodn/know-your-planet/issues)) :)

## Aider au développement de l'application

La stack technique est détaillée un peu plus bas.

Si vous souhaitez ajouter une fonctionnalité:
- commentez l'Issue en question pour donner votre point de vue (ou créez l'Issue si elle n'existe pas encore), et on discutera ensemble de la meilleur façon de procéder
- créez ensuite une PR et demandez une review (relecture)

## Informations supplémentaires

### Stack technique

#### Backend

- Une backend en Python Django
  - API avec Django Rest Framework
  - console Admin
- Une base de donnée PostgreSQL

#### Frontend

- Un frontend en Vue.js

#### DevOps

- Le backend est hébergé sur Heroku (free tier)
- Le frontend est hébergé sur Netlify (free tier)

### Lancer le projet en local

#### Installer l'application

- Vous devez avoir Python 3.7 installé sur votre machine
- Clonez le code en local
    ```
    git clone git@github.com:raphodn/know-your-planet.git
    ```
- Installez les dépendances du Backend
    ```
    pip install -r requirements.txt
    ```
- Installer le pre-commit git hook
    ```
    pre-commit install
    ```
- Dupliquer le fichier `.env.example` et le renommer en `.env`
- Lancez les migrations
    ```
    python manage.py migrate
    ```
- Chargez la base de donnée
    ```
    python manage.py loaddata api/data/categories.yaml
    python manage.py loaddata api/data/tags.yaml
    python manage.py loaddata api/data/questions.yaml
    python manage.py loaddata api/data/quizzes.yaml
    ```
- Installez les dépendances du Frontend
    ```
    cd frontend
    yarn install
    ```

#### Lancer l'application

##### Lancer le Backend

```
python manage.py runserver
```

Le Backend sera accessible à l'url `http://localhost:8000`

##### Lancer le Frontend

```
cd frontend
yarn serve
```

Le Frontend sera accessible à l'url `http://localhost:8080`

#### Accéder à la console admin

Créez d'abord un utilisateur admin
```
python manage.py createsuperuser --username admin@email.com
```

Connectez-vous ensuite sur `http://localhost:8000/admin`

#### Autres commandes utiles

Exporter les questions de la base au format YAML
```
python manage.py dumpdata api.question --format=yaml --pretty > api/data/questions.yaml
```
