# Know Your Planet 🌍

Mieux appréhender les limites de notre planète, à travers des questions simples et sourcées.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [But](#but)
- [Stack technique](#stack-technique)
  - [Backend](#backend)
  - [Frontend](#frontend)
  - [DevOps](#devops)
- [Infos supplémentaires](#infos-suppl%C3%A9mentaires)
- [Lancer le projet en local](#lancer-le-projet-en-local)
  - [Installer l'application](#installer-lapplication)
  - [Lancer l'application](#lancer-lapplication)
    - [Lancer le Backend](#lancer-le-backend)
    - [Lancer le Frontend](#lancer-le-frontend)
  - [Accéder à la console admin](#acc%C3%A9der-%C3%A0-la-console-admin)
  - [Autres commandes utiles](#autres-commandes-utiles)
- [Idées](#id%C3%A9es)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## But

- Rassembler un ensemble de connaissances sous forme de questions (QCM uniquement pour l'instant)
- Couvrir un large panel de sujets: climat, biodiversité, énergie, consommation, ...
- Des questions avec différents niveaux de difficultés, pour sensibiliser ou se perfectionner
- Une rigueur scientifique dans le choix des questions, et surtout dans les explications apportées autour de la réponse
- Une base de donnée facilement accessible et editable
- Une application simple pour une prise en main rapide

## Stack technique

### Backend

- Une backend en Python Django
  - API avec Django Rest Framework
  - console Admin
- Une base de donnée PostgreSQL
- Un fichier YAML qui regroupe toutes les questions

### Frontend

- Un frontend en Vue.js

### DevOps

- Le backend est hébergé sur Heroku (free tier)
- Le frontend est hébergé sur Netlify (free tier)

## Infos supplémentaires

- Les questions sont stockées au format YAML, dans le fichier `api/data/questions.yaml`
- Le code et les questions sont en open-source: venez nous aider !

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
python manage.py dumpdata api.question --format=yaml --pretty > api/data/questions.yaml
```

### Contribuer

TODO: fichier `CONTRIBUTION.md`

Installer le pre-commit git hook
```
pre-commit install
```

## Idées

- Proposer à l'utilisateur un feedback rapide sur la question (👍, 👎, voire 💬)
- Rajouter de nouveaux formats de questions: Vrai/Faux par exemple
- Mode quizz ("10 questions climat")
- Pouvoir mieux filtrer les questions (catégorie, tags, difficulté)
- ...
