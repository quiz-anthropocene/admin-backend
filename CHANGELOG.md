# Changelog

Un suivi à jour des modifications apportées à ce projet (cf [Keep a Changelog](https://keepachangelog.com/en/1.0.0/))

## A venir

- [Data] Rajouter d'avantage de questions

## [0.1.0] - 2020-03-08

### Ajouté

- [Data] 10 questions dans la base de donnée
- [Backend] Un modèle Question pour stocker les questions à choix multiples
- [Backend] Une ressource API `/questions` pour récupérer toutes les questions
- [Backend] Une ressource API `/questions/:id` pour récupérer une question par id
- [Backend] Une ressource API `/questions/random` pour récupérer une question au hasard
- [Backend] Chaque question possède 1 seul catégorie
- [Backend] Une console admin fournie par Django
- [Backend] Les questions sont écrites dans un fichier YAML avant d'être loadés en base de donnée
- [Frontend] Une page principale avec l'ensemble des questions, avec un filtre simple par catégorie
- [Frontend] Une page par question, avec la possibilité d'y répondre et de voir ensuite la réponse
- [Frontend] Un début de page A propos avec un lien vers le repo Github
- [DevOps] Séparation des variables d'environment (local & prod)
- [DevOps] Déploiement du Backend (Django API & Admin) sur Heroku
- [DevOps] Déploiement du Frontend (Vuejs) sur Netlify
- [Documentation] Un fichier README
- [Documentation] Un fichier CHANGELOG
