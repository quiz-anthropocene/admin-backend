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
  - [Schéma d'architecture](#sch%C3%A9ma-darchitecture)
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

Le Backend sert pour valider la donnée, ainsi que d'endpoint pour les stats.

#### Frontend

- Un Frontend en Vue.js
- Bootstrap 4

La donnée est lue directement depuis les fichiers yaml dans le dossier `/data`.

#### DevOps

- Le Backend est hébergé sur Scalingo
- Le Frontend est hébergé sur Netlify (free tier)
- CI/CD avec Github Actions
- Cron pour automatiser certaines tâches avec Github Actions

### Schéma d'architecture

Voir dans le dossier `/data/architecture`

### Lancer le projet en local

#### Installer l'application

- Vous devez avoir Python 3.9 & Pipenv installés sur votre machine.
- Clonez le code en local (vous pouvez aussi Fork le projet si vous prévoyez d'y apporter des modifications et effectuer une PR)
    ```
    git clone git@github.com:raphodn/know-your-planet.git
    ```
- Installez les dépendances du Backend
    ```
    cd backend
    pipenv install --dev
    ```
- Dupliquer le fichier `backend/.env.example` et le renommer en `backend/.env`
- Installez [PostgreSQL](https://www.postgresql.org)
- Créez la base de donnée
    ```
    psql -c "CREATE USER know_your_planet_team WITH PASSWORD 'password'"
    psql -c "CREATE DATABASE know_your_planet OWNER know_your_planet_team"
    psql -c "ALTER USER know_your_planet_team CREATEDB"
    ```
- Lancez les migrations
    ```
    pipenv run python manage.py migrate
    ```
- Chargez la base de donnée
    ```
    pipenv run python manage.py init_db --with-sql-reset
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
cd backend
pipenv run python manage.py runserver
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
cd backend
pipenv run python manage.py createsuperuser --username admin@email.com --email admin@email.com
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

Rappel : pour le backend, toutes les commandes doivent commencer par `pipenv run`

#### Backend

Importer toute la donnée dans la base de donnée
```
python manage.py init_db --with-sql-reset
```

Importer les questions dans la base de donnée
```
// ne marche pas car les fichiers dans le dossier /data sont "applatis" (flat)
python manage.py loaddata ../data/questions.yaml

// marche seulement si les questions ont été supprimées en amont
python manage.py loaddata ../data/questions.yaml --model=question --format=yaml-pretty-flat
```

Exporter les questions de la base de donnée au format YAML
```
// on utilise un format légerement modifier pour simplifier le fichier
python manage.py dumpdata api.question --output=../data/questions.yaml  --format=yaml-pretty-flat

// mais il est toujours possible de faire un dumpdata normal
python manage.py dumpdata api.question --output=../data/questions.yaml
```

Réinitialiser les stats d'une question
```
python manage.py reset_question_stats <question_id>
```

Réinitialiser complètement la base de donnée
```
python manage.py reset_db // django-extensions
python manage.py migrate
python manage.py init_db --with-sql-reset
```

Queries M2M
```
qz1 = Quiz.objects.first()

qz1.questions.all()
qz1.quizquestion_set.all()

qz1.relationships.all()
qz1.from_quizs.all()
qz1.to_quizs.all()

q = Question.objects.first()

q.quizzes.all()
q1.quizquestion_set.all()
```

Générer le graph des modèles
```
pip install pygraphviz
python manage.py graph_models -a -X ContentType,LogEntry,AbstractUser,User,AbstractBaseSession,Session,Group,Permission -o graph.png
```

#### Frontend

Lancer le Frontend "en mode production"
```
yarn build
// installer le package 'serve' : npm install -g serve
serve -s dist
```

Launch the Vue.js UI
```
vue ui
```

#### Autres

Mettre à jour l'instance Metabase sur Heroku
- https://www.metabase.com/docs/latest/operations-guide/running-metabase-on-heroku.html
