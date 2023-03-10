<p align="center">
  <a href="https://quizanthropocene.fr/en">
    <img alt="QuizAnthropocene" height="125" src="https://avatars.githubusercontent.com/u/105566092?s=200&v=4">
  </a>
  <br>
  <!-- base64 flags are available at https://www.phoca.cz/cssflags/ -->
    <a href="https://github.com/quiz-anthropocene/admin-backend/blob/master/README.md">
<img height="20px" src="https://img.shields.io/badge/EN-flag.svg?color=555555&style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB2aWV3Qm94PSIwIDAgNjAgMzAiIGhlaWdodD0iNjAwIj4NCjxkZWZzPg0KPGNsaXBQYXRoIGlkPSJ0Ij4NCjxwYXRoIGQ9Im0zMCwxNWgzMHYxNXp2MTVoLTMwemgtMzB2LTE1enYtMTVoMzB6Ii8+DQo8L2NsaXBQYXRoPg0KPC9kZWZzPg0KPHBhdGggZmlsbD0iIzAwMjQ3ZCIgZD0ibTAsMHYzMGg2MHYtMzB6Ii8+DQo8cGF0aCBzdHJva2U9IiNmZmYiIHN0cm9rZS13aWR0aD0iNiIgZD0ibTAsMGw2MCwzMG0wLTMwbC02MCwzMCIvPg0KPHBhdGggc3Ryb2tlPSIjY2YxNDJiIiBzdHJva2Utd2lkdGg9IjQiIGQ9Im0wLDBsNjAsMzBtMC0zMGwtNjAsMzAiIGNsaXAtcGF0aD0idXJsKCN0KSIvPg0KPHBhdGggc3Ryb2tlPSIjZmZmIiBzdHJva2Utd2lkdGg9IjEwIiBkPSJtMzAsMHYzMG0tMzAtMTVoNjAiLz4NCjxwYXRoIHN0cm9rZT0iI2NmMTQyYiIgc3Ryb2tlLXdpZHRoPSI2IiBkPSJtMzAsMHYzMG0tMzAtMTVoNjAiLz4NCjwvc3ZnPg0K">
  </a>
  <a href="https://github.com/quiz-anthropocene/admin-backend/tree/master/locale/fr/README_fr.md">
    <img height="20px" src="https://img.shields.io/badge/FR-flag.svg?color=555555&style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA5MDAgNjAwIj4NCjxwYXRoIGZpbGw9IiNlZDI5MzkiIGQ9Im0wLDBoOTAwdjYwMGgtOTAweiIvPg0KPHBhdGggZmlsbD0iI2ZmZiIgZD0ibTAsMGg2MDB2NjAwaC02MDB6Ii8+DQo8cGF0aCBmaWxsPSIjMDAyMzk1IiBkPSJtMCwwaDMwMHY2MDBoLTMwMHoiLz4NCjwvc3ZnPg0K">
  </a>
  </br>
</p>


# Contribute

Thank you for helping us!

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [How can I help?](#how-can-i-help)
  - [Add or modify questions](#add-or-modify-questions)
  - [Suggest improvements to the application](#suggest-improvements-to-the-application)
  - [Contribute to the development of the application](#contribute-to-the-development-of-the-application)
- [Additional informations](#additional-informations)
  - [Technical stack](#technical-stack)
    - [Backend](#backend)
    - [Frontend](#frontend)
    - [DevOps](#devops)
  - [Architecture diagram](#architecture-diagram)
  - [Start the project locally](#start-the-project-locally)
    - [Install the application](#install-the-application)
    - [Start the application](#start-the-application)
    - [Access the admin console](#access-the-admin-console)
  - [Start tests](#start-tests)
  - [Translation](#translation)
  - [In the code](#in-the-code)
  - [Add a new language](#add-a-new-language)
  - [Translatation improvement or addition in an existing language](#translatation-improvement-or-addition-in-an-existing-language)
  - [Other useful commands](#other-useful-commands)
    - [Backend commands](#backend-commands)
    - [Other commands](#other-commands)
    - [Windows specific](#windows-specific)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## How can I help?

You can contribute to the project in many ways:

- Contribute to the questions database:
    - Add new questions
    - Propose modifications on existing questions

- Contribute to the application:
    - Notify us about bugs
    - Propose improvements (through Github Issues)
    - Help the development of the application (through Github Issues and Pull Requests)
    - Help with translation

### Add or modify questions

Every question (finalised or in draft) is currently in a shared plateform (Notion.so), which is regularly synchronised with the database.

You can see an export of the whole databse of the application in folder `/data` (Note : this is not the database, just an export).

You can propose new questions directly in [Contribuer](https://quizanthropocene.fr/contribuer) (TODO translate page and update link).

Questions are then validated in the shared plateform.

### Suggest improvements to the application

Did you find a bug? Do you find the interface counter-intuitive, or you have an idea to improve the design?

There are 2 options to share your feedback:
- via [Contribuer](https://quizanthropocene.fr/contribuer) (TODO translate page and update link).
- on Github Issues by creating a new issue ([here](https://github.com/quiz-anthropocene/know-your-planet/issues)).

### Contribute to the development of the application

_The technical stack is detailed further down._

You can help with code review, documentation, add tests, improve design, add new features...

If you want to add a new feature:
- comment an Issue to give your rationale or create a new one if it does not exist, we will then discuss in the Issue thread on how to proceed.
- Start coding! and create a new PR with a review request

## Additional informations

### Technical stack

#### Backend

- Our Backend uses Python Django :
  - API with Django Rest Framework
  - Admin console
- PostgreSQL database

We use the backend to:
- validate data coming from the share plateform
- Create new quizzes
- have an endpoint for stats

#### Frontend

repo : [quiz-anthropocene/public-frontend](https://github.com/quiz-anthropocene/public-frontend)

- Our Frontend uses Vue.js
- Bootstrap 4

Currently, the data is directly read from yaml files in folder `/data`. An API is under construction

#### DevOps

- Our Backend is hosted on Scalingo
- Our Frontend is hosted on Netlify (free tier)
- CI/CD with Github Actions
- Cron jobs with Github Actions

### Architecture diagram

View folder [quiz-anthropocene/public-frontend/data/architecture](https://github.com/quiz-anthropocene/public-frontend/tree/master/data/architecture)

### Start the project locally

#### Install the application

- You need Python 3.9 & Pipenv already installed.
- Clone the code locally (you can also Fork the project if you plan to add modifications and do PR)
    ```
    git clone git@github.com:quiz-anthropocene/know-your-planet.git
    ```
- Install Backend dependencies
    ```
    cd backend
    pipenv sync
    ```
- Duplicate file `backend/.env.example` and rename into `backend/.env`
- Install [PostgreSQL](https://www.postgresql.org)
- Build the database
    ```
    // optional: dropdb quiz_anthropocene
    psql -c "CREATE USER quiz_anthropocene_team WITH PASSWORD 'password'"
    psql -c "CREATE DATABASE quiz_anthropocene OWNER quiz_anthropocene_team"
    psql -c "GRANT ALL PRIVILEGES ON DATABASE quiz_anthropocene to quiz_anthropocene_team"
    psql -c "ALTER USER quiz_anthropocene_team CREATEROLE CREATEDB"
    ```
    \* If you haven't created a USER to login to postgresql, please do before the previous commands. Alternatively, during postgresql installation, you need to choose a superuser (postgres) password and you just need to add '-U postgres' to the previous commands.
- Start migrations
    ```
    pipenv run python manage.py migrate
    ```
    \* Go to the Windows section if you have an issue with a Windows environment
- Load the database
    ```
    pipenv run python manage.py init_db_from_yaml --with-sql-reset
    ```
- Install pre-commit git hook
    ```
    pre-commit install
    ```
\* Go to the Windows section if you have an issue with a Windows environment

#### Start the application

```
cd backend
pipenv run python manage.py runserver
```

You can reach the backen at url `http://localhost:8000`

You can reach the API documentation at url `http://localhost:8000/api/docs/`

#### Access the admin console

First start by creating an admin user
```
cd backend
pipenv run python manage.py createsuperuser --username admin@email.com --email admin@email.com
```

Start the backend and go to url `http://localhost:8000/django`

### Start tests

Tests
```
pipenv run python manage.py test
```

Linting ? with pre-commit

### Translation

First install `gettext`

The tranlation files can be found under `/locale`

### In the code

Use tags `{% translate "Word" %}`

Then update `.po` files
```
python manage.py makemessages --all
```

### Add a new language

https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes

```
python manage.py makemessages -l <LANGUAGE_CODE>
```

Add the language code in `settings.py`

### Translatation improvement or addition in an existing language

Use [Poedit](https://poedit.net/) to simplify your job.

It will update the `.po` files in `/locale`.

Then compile the `.po` files into `.mo`
```
python manage.py compilemessages
```

### Other useful commands

Note : for the backend, every command should start with `pipenv run`

#### Backend commands

Import the whole database
```
python manage.py init_db_from_yaml --with-sql-reset
```

Import questions into the database
```
// doesn't work since files in /data are "flat"
python manage.py loaddata ../data/questions.yaml

// works only if questions have been deleted previously in database
python manage.py loaddata ../data/questions.yaml --model=question --format=yaml-pretty-flat
```

Export questions from database to YAML files
```
// We use a slightly different format to simplify the files
python manage.py dumpdata api.question --output=../data/questions.yaml  --format=yaml-pretty-flat

// but it's still possible to do a normal data dump
python manage.py dumpdata api.question --output=../data/questions.yaml
```

Reinitialise statistics of a question
```
python manage.py reset_question_stats <question_id>
```

Reinitialise the whole database
```
python manage.py reset_db // django-extensions
python manage.py migrate
python manage.py init_db_from_yaml --with-sql-reset
```

Import a PGSQL dump
```
// if it's a .tar.gz, run first
tar -xvzf <dump_name>.tar.gz

pg_restore -d quiz_anthropocene --clean --no-owner --no-privileges <dump_name>.pgsql

// if there are permission issues
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

Generate the model graph
```
pip install pygraphviz
python manage.py graph_models -a -X ContentType,LogEntry,AbstractUser,User,AbstractBaseSession,Session,Group,Permission -o graph.png
```

Update packages
```
pipenv install --dev
```

#### Other commands

Update the Metabase instance on Heroku
- https://www.metabase.com/docs/latest/operations-guide/running-metabase-on-heroku.html

Resize images (PNG)
- Install [pngquant](https://pngquant.org/)
- Run the software on a specific file: `pngquant -f --ext .png <filename>`
- Run the software fol all files in a folder: `pngquant -f --ext .png **/*.png`

#### Windows specific

You might have encoding issues with Windows during database import for example
```
pipenv run python -X utf8 manage.py init_db_from_yaml --with-sql-reset
```

- Install pre-commit
```
pip install pre-commit
```

Error `UnicodeDecodeError: charmap codec can't decode byte`

- Add `-X utf8`
