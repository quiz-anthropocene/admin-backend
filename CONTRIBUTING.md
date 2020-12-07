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
    - [Backend](#backend)
    - [Frontend](#frontend)
    - [DevOps](#devops)
  - [Lancer le projet en local](#lancer-le-projet-en-local)
    - [Installer l'application](#installer-lapplication)
    - [Lancer l'application](#lancer-lapplication)
      - [Lancer le Backend](#lancer-le-backend)
      - [Lancer le Frontend](#lancer-le-frontend)
    - [Accéder à la console admin](#acc%C3%A9der-%C3%A0-la-console-admin)
  - [Lancer les tests](#lancer-les-tests)
    - [Lancer les tests du Backend](#lancer-les-tests-du-backend)
    - [Lancer les tests du Frontend](#lancer-les-tests-du-frontend)
  - [Autres commandes utiles](#autres-commandes-utiles)

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

### Rajouter ou modifier des questions

Toutes les questions (finalisées ou en cours de création) sont actuellement dans un fichier partagé (type Google Sheet), que l'on synchronise régulièrement avec la base de donnée.

Un export de toutes les questions de la base de donnée de l'application peuvent être vues dans le fichier `data/questions.yaml` (Rappel: ce n'est pas la source de la base de donnée, seulement un export).

Vous pouvez proposer de nouvelles questions via la page [Contribuer](https://quizanthropocene.fr/contribuer) de l'application.

La validation des questions se fait ensuite dans le fichier partagé.

### Proposer des améliorations de l'application

Vous avez vu un bug ? Vous trouvez l'app contre-intuitive, ou simplement avez une idée pour rendre le design plus beau/propre ?

Il y a deux options pour remonter ces informations:
- via la page [Contribuer](https://quizanthropocene.fr/contribuer) de l'application
- ou créer une Issue dans l'interface Github du projet ([ici](https://github.com/raphodn/know-your-planet/issues))

### Aider au développement de l'application

_La stack technique est détaillée un peu plus bas._

Relecture de code, documentation, rajouter des tests, design, ajouter une fonctionnalité, etc

Si vous souhaitez ajouter une fonctionnalité:
- commentez l'Issue en question pour donner votre point de vue (ou créez l'Issue si elle n'existe pas encore), et on discutera ensemble de la meilleur façon de procéder
- créez ensuite une PR et demandez une review (relecture)

## Informations supplémentaires

### Stack technique

#### Backend

- Un Backend en Python Django:
  - API avec Django Rest Framework
  - console Admin
- Une base de donnée PostgreSQL

Le Backend sert pour valider la donnée, ainsi que comme endpoint pour les stats.

#### Frontend

- Un Frontend en Vue.js
- Bootstrap 4

La donnée est lue directement depuis les fichiers yaml dans le dossier `/data`.

#### DevOps

- Le Backend est hébergé sur Scalingo
- Le Frontend est hébergé sur Netlify (free tier)
- CI/CD avec CircleCI

### Lancer le projet en local

#### Installer l'application

- Vous devez avoir Python 3.7 installé sur votre machine (environment virtuel (`venv` par exemple) recommandé)
- Clonez le code en local (vous pouvez aussi Fork le projet si vous prévoyez d'y apporter des modifications et effectuer une PR)
    ```
    git clone git@github.com:raphodn/know-your-planet.git
    ```
- Installez les dépendances du Backend
    ```
    pip install -r requirements.txt
    ```
- Dupliquer le fichier `.env.example` et le renommer en `.env`
- Installez [PostgreSQL](https://www.postgresql.org)
- Créez la base de donnée
    ```
    psql -c "CREATE USER know_your_planet_team"
    psql -c "CREATE DATABASE know_your_planet OWNER know_your_planet_team"
    psql -c "ALTER USER know_your_planet_team CREATEDB"
    ```
- Lancez les migrations
    ```
    python manage.py migrate
    ```
- Chargez la base de donnée
    ```
    python manage.py loaddata data/configuration.yaml
    python manage.py loaddata data/categories.yaml
    python manage.py loaddata data/tags.yaml
    python manage.py loaddata data/questions.yaml
    python manage.py loaddata data/quizzes.yaml
    ```
- Installez les dépendances du Frontend
    ```
    cd frontend
    yarn install
    ```
- Dupliquer le fichier `frontend/.env.example` et le renommer en `frontend/.env`
- Installer le pre-commit git hook
    ```
    pre-commit install
    ```

#### Lancer l'application

##### Lancer le Backend (optionnel)

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

Lancez le Backend, et connectez-vous sur `http://localhost:8000/admin`

### Lancer les tests

#### Lancer les tests du Backend

Tests
```
python manage.py test
```

Coverage
```
coverage run manage.py test

// report
coverage report
coverage html
```

Linting avec black et flake8 (pre-commit hook)

#### Lancer les tests du Frontend

Tests
```
yarn test:e2e
```

Linting
```
yarn lint
```

### Autres commandes utiles

Exporter les questions de la base au format YAML
```
python manage.py dumpdata api.question --format=yaml-pretty --output=data/questions.yaml
```

Importer les questions dans la base
```
python manage.py loaddata data/questions.yaml
```

Réinitialiser les stats d'une question
```
python manage.py reset_question_stats <question_id>
```

Lancer le Frontend "en mode production"
```
cd frontend
yarn build
// installer le package 'serve' : npm install -g serve
serve -s dist
```

Launch the Vue.js UI
```
cd frontend
vue ui
```

Mettre à jour l'instance Metabase sur Heroku
- https://www.metabase.com/docs/latest/operations-guide/running-metabase-on-heroku.html
