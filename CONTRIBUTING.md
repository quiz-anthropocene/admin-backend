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
    - [Accéder à la console admin](#acc%C3%A9der-%C3%A0-la-console-admin)
  - [Lancer les tests](#lancer-les-tests)
  - [Traduction](#traduction)
  - [Autres commandes utiles](#autres-commandes-utiles)
    - [Commandes Backend](#commandes-backend)
    - [Commandes Autres](#commandes-autres)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Comment aider ?

Il y a plusieurs aspects du projet qui ont besoin d'aide :

- La base de donnée de questions :
    - rajouter de nouvelles questions
    - proposer des modifications sur des questions existantes
- L'application :
    - remonter les bugs
    - faire des propositions d'améliorations (grâce aux Issues Github)
    - aider à développer l'application (grâce aux Issues et Pull Requests Github)
    - aider à traduire l'application

### Rajouter ou modifier des questions

Toutes les questions (finalisées ou en cours de création) sont actuellement dans un espace partagé (Notion.so), que l'on synchronise régulièrement avec la base de donnée.

Un export de toute la base de donnée de l'application peut être vu dans le dossier `/data` (Rappel : ce n'est pas la source de la base de donnée, seulement un export).

Vous pouvez proposer de nouvelles questions via la page [Contribuer](https://quizanthropocene.fr/contribuer) de l'application.

La validation des questions se fait ensuite dans l'espace partagé.

### Proposer des améliorations de l'application

Vous avez vu un bug ? Vous trouvez l'app contre-intuitive, ou simplement avez une idée pour rendre le design plus beau/propre ?

Il y a deux options pour remonter ces informations :
- via la page [Contribuer](https://quizanthropocene.fr/contribuer) de l'application
- ou créer une Issue dans l'interface Github du projet ([ici](https://github.com/quiz-anthropocene/know-your-planet/issues))

### Aider au développement de l'application

_La stack technique est détaillée un peu plus bas._

Relecture de code, documentation, rajouter des tests, design, ajouter une fonctionnalité, etc

Si vous souhaitez ajouter une fonctionnalité :
- commentez l'Issue en question pour donner votre point de vue (ou créez l'Issue si elle n'existe pas encore), et on discutera ensemble de la meilleur façon de procéder
- créez ensuite une PR et demandez une review (relecture)

## Informations supplémentaires

### Stack technique

#### Backend

- Un Backend en Python Django :
  - API avec Django Rest Framework
  - console Admin
- Une base de donnée PostgreSQL

Le Backend sert à :
- valider la donnée provenant de l'espace partagé
- de créer les quiz
- d'endpoint pour les stats

#### Frontend

repo : [quiz-anthropocene/public-frontend](https://github.com/quiz-anthropocene/public-frontend)

- Un Frontend en Vue.js
- Bootstrap 4

La donnée est lue directement depuis les fichiers yaml dans le dossier `/data`.

#### DevOps

- Le Backend est hébergé sur Scalingo
- Le Frontend est hébergé sur Netlify (free tier)
- CI/CD avec Github Actions
- Cron pour automatiser certaines tâches avec Github Actions

### Schéma d'architecture

Voir dans le dossier [quiz-anthropocene/public-frontend/data/architecture](https://github.com/quiz-anthropocene/public-frontend/tree/master/data/architecture)

### Lancer le projet en local

#### Installer l'application

- Vous devez avoir Python 3.9 & Pipenv installés sur votre machine.
- Clonez le code en local (vous pouvez aussi Fork le projet si vous prévoyez d'y apporter des modifications et effectuer une PR)
    ```
    git clone git@github.com:quiz-anthropocene/know-your-planet.git
    ```
- Installez les dépendances du Backend
    ```
    cd backend
    pipenv sync
    ```
- Dupliquer le fichier `backend/.env.example` et le renommer en `backend/.env`
- Installez [PostgreSQL](https://www.postgresql.org)
- Créez la base de donnée
    ```
    // optional: dropdb quiz_anthropocene
    psql -c "CREATE USER quiz_anthropocene_team WITH PASSWORD 'password'"
    psql -c "CREATE DATABASE quiz_anthropocene OWNER quiz_anthropocene_team"
    psql -c "GRANT ALL PRIVILEGES ON DATABASE quiz_anthropocene to quiz_anthropocene_team"
    psql -c "ALTER USER quiz_anthropocene_team CREATEROLE CREATEDB"
    ```
    \* Si vous n'avez pas créé de USER pour accéder à postgresql, faites le avant les commandes précédentes. Alternativement, lors de l'installation de postgresql, l'utilisateur doit choisir un mot de passe superuser (postgres) et il suffit de rajouter '-U postgres' aux commandes précédentes.
- Lancez les migrations
    ```
    pipenv run python manage.py migrate
    ```
    \* Voir section Windows à la fin si cette commande pose problème
- Chargez la base de donnée
    ```
    pipenv run python manage.py init_db_from_yaml --with-sql-reset
    ```
- Installer le pre-commit git hook
    ```
    pre-commit install
    ```
\* Voir section Windows à la fin si cette section pose problème

#### Lancer l'application

```
cd backend
pipenv run python manage.py runserver
```

Le Backend sera accessible à l'url `http://localhost:8000`

La doc de l'API est visible à l'url `http://localhost:8000/api/docs/`

#### Accéder à la console admin Django

Créez d'abord un utilisateur admin
```
cd backend
pipenv run python manage.py createsuperuser --username admin@email.com --email admin@email.com
```

Lancez le Backend, et connectez-vous sur `http://localhost:8000/django`

### Lancer les tests

Tests
```
pipenv run python manage.py test
```

Linting ? Avec le pre-commit

### Traduction

Vous devez d'abord installer `gettext`

Les fichiers de traductions se trouvent dans le dossier `/locale`

Mettre à jour les fichiers `.po`
```
python manage.py makemessages --all
```

Compiler les fichiers `.po` en `.mo`
```
python manage.py compilemessages
```

### Autres commandes utiles

Rappel : pour le backend, toutes les commandes doivent commencer par `pipenv run`

#### Commandes Backend

Importer toute la donnée dans la base de donnée
```
python manage.py init_db_from_yaml --with-sql-reset
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
python manage.py init_db_from_yaml --with-sql-reset
```

Importer un dump PGSQL
```
// if it's a .tar.gz, run first
tar -xvzf <dump_name>.tar.gz

pg_restore -d quiz_anthropocene --clean --no-owner --no-privileges <dump_name>.pgsql

// si il y a ensuite des soucis de permissions
for tbl in `psql -qAt -c "select tablename from pg_tables where schemaname = 'public';" quiz_anthropocene` ; do  psql -c "alter table \"$tbl\" owner to quiz_anthropocene_team" quiz_anthropocene ; done
for tbl in `psql -qAt -c "select sequence_name from information_schema.sequences where sequence_schema = 'public';" quiz_anthropocene` ; do  psql -c "alter sequence \"$tbl\" owner to quiz_anthropocene_team" quiz_anthropocene ; done
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

q.quizs.all()
q1.quizquestion_set.all()
```

Générer le graph des modèles
```
pip install pygraphviz
python manage.py graph_models -a -X ContentType,LogEntry,AbstractUser,User,AbstractBaseSession,Session,Group,Permission -o graph.png
```

Update packages
```
pipenv install --dev
```

#### Commandes Autres

Mettre à jour l'instance Metabase sur Heroku
- https://www.metabase.com/docs/latest/operations-guide/running-metabase-on-heroku.html

Réduire la taille des images (PNG)
- Installer [pngquant](https://pngquant.org/)
- Lancer sur un fichier donné : `pngquant -f --ext .png <filename>`
- Ou lancer sur tous les fichiers d'un dossier : `pngquant -f --ext .png **/*.png`

#### Spécifique pour Windows

Windows peut poser des soucis d'encodage, pour l'étape de charger la base de donnée, entrez la commande
```
pipenv run python -X utf8 manage.py init_db_from_yaml --with-sql-reset
```

- Installer pre-commit
```
pip install pre-commit
```

Erreur `UnicodeDecodeError: charmap codec can't decode byte`

- Rajoutez `-X utf8`
