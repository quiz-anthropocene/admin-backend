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
- Installez les dépendances
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

### Lancer l'application

```
python manage.py runserver
```

Elle sera accessible à l'url `http://localhost:8000`

### Accéder à la console admin

Créez d'abord un utilisateur admin
```
python manage.py createsuperuser --username admin@email.com
```

Connectez-vous sur `http://localhost:8000/admin`

## Qui sommes-nous ?

A venir
