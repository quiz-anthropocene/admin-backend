# Changelog

Un suivi à jour des modifications apportées à ce projet (cf [Keep a Changelog](https://keepachangelog.com/en/1.0.0/))

## A venir

Des pistes dans [README.md#idées](README.md#idées)

## [1.1.0] - 2020-12-06

- [Data] Nouveau dashboard Metabase connecté à la base de donnée de Scalingo
- [Backend] Nouveau modèle `Configuration` pour stocker des variables globales de l'application. Certains champs sont modifiables.
- [Backend] RichTextEditor pour les champs `introduction` & `conclusion` du modèle `Quiz` (pour pouvoir aller à la ligne)
- [Backend] Nouveau statut "Ecartée temporairement" pour les questions
- [Backend] Enlève le champ `publish` du modèle `Question` (on regarde maintenant seulement sont `validation_status`)
- [Backend] Créer les nouveaux tags automatiquement lors de l'import depuis Notion

- [Backend] Automatiser le lancement des tâches (import depuis Notion, export vers Github, aggrégation des Daily Stats)
- [Backend] Exporter certains stats à chaque export de la donnée (pour éviter d'avoir un endpoint API et d'y faire des appels)
- [Frontend] Boutons de partage sur les réseaux sociaux à la fin d'un quiz

## [1.0.0] - 2020-11-29

- [Data] Ajout d'images de laydgeur
- [Data] Ajout de Bon Pote dans les soutiens
- [DevOps] Migration du backend de Heroku vers Scalingo
- [Backend] Ajout d'un champ `question_count` dans le modèle `QuizAnswerEvent` (pour garder des stats de réussites claires même si le nombre de questions du quiz change)
- [Backend] Toujours mettre `publish=True` lors de l'import si la question est Validée (bug fix)
- [Frontend] Afficher les 3 derniers quizs sur la page d'accueil
- [Frontend] Ajout des filtres sur la page des quizs

## TODO

## [0.7.0] - en cours

### Ajouté

- [Admin] Graph affichant le nombre de réponses aux quizs par jour
- [DevOps] Linting automatique du code backend avec `flake8`, `black` et un pre-commit git hook
- [DevOps] Ajout d'un fichier `CONTRIBUTING.md`

### Modifié

- [Backend] Renommé le modèle `QuestionCategory` en `Category`
- [Backend] Renommé le modèle `QuestionTag` en `Tag`

## [0.6.0] - 2020-04-17

### Ajouté

- [Backend] Un modèle `Quiz` pour stocker les quizs
- [Backend] Un modèle `QuizStat` pour avoir des stats d'usage sur les quizs
- [Frontend] Les choix des questions s'affichent dans le désordre (pour les questions qui le permettent)
- [Frontend] Une page Tags avec la liste des tags
- [Frontend] Une page Tag avec la liste des questions pour le tag donné
- [Frontend] Une page Auteurs avec la liste des auteurs
- [Frontend] Une page Auteur avec la liste des questions pour l'auteur donné
- [Frontend] Une page Quizs avec la liste des quizs
- [Frontend] Une page Quiz avec un premier workflow complet pour répondre aux questions les unes après les autres, et avoir un score/résultat à la fin

### Modifié

- [Frontend] Refactoring des appels api avec l'ajout de vuex. Loader global.
- [Frontend] Amélioré l'affichage de la question, des choix et de la réponse (jeu de couleur, components, css, ...)
- [Frontend] Cacher le sous-titre de l'application sur petits écrans
- [DevOps] l'url netlify a changé de `know-your-planet.netlify.com` à `know-your-planet.netlify.app`

## [0.5.0] - 2020-04-05

### Ajouté

- [Admin] Fonctions d'export de la donnée (csv, json, yaml)
- [Admin] Graph affichant le nombre de réponses par jour
- [Backend] Un modèle `QuestionCategory` pour stocker les catégories (au lieu d'un champ)
- [Backend] Un modèle `QuestionTag` pour stocker les tags

### Modifié

- [Backend] Le champ catégorie passe d'un CharField à une ForeignKey
- [Backend] Utilisation de URLField pour les champ url de `Question`
- [Frontend] Rajout d'une action 'commentaire' sur la page de contribution

## [0.4.0] - 2020-03-27

### Ajouté

- [Backend] Un modèle `Contribution` pour stocker les contributions
- [Backend] Une ressource API `/contribute` pour recevoir les contributions
- [Frontend] Affiche un message légèrement aléatoire pour chaque réponse correcte
- [Frontend] Une page Catégories avec la liste des catégories
- [Frontend] Une page Catégorie avec la liste des questions pour la catégorie donnée
- [Frontend] Ajout de la librarie CSS Bootstrap. Cleanup du CSS.
- [Frontend] Ajout d'un footer avec des liens vers les autres pages
- [Frontend] Page de contribution
- [Frontend] Refactoring des components et du routing Vue.js
- [Documentation] Framaboard

### Modifié

- [Data] Ajout d'un maximum d'images aux questions existantes
- [Frontend] Refonte de la page principale

## [0.3.0] - 2020-03-22

### Ajouté

- [Backend] Ajout d'un champs `answer_image_link` dans le modèle Question
- [Frontend] Une page Stats pour afficher quelques les chiffres basiques de l'application (nombre de questions, nombre de réponses, ...)
- [Frontend] Un bouton "Autre question dans la même catégorie"
- [Frontend] Affiche l'auteur et les statistiques de la question (dans la réponse)

### Modifié

- [DevOps] Ajout de la commande loaddata au Procfile
- [Frontend] Typo dans la description de l'application

## [0.2.0] - 2020-03-11

### Ajouté

- [Data] Ajout de toutes les questions (80+)
- [Backend] Un modèle `QuestionStats` pour commencer à avoir des stats d'usage (nombre de réponses par question, nombre de réponses correctes par question, ...)
- [Backend] Ajout d'un champs `author` dans le modèle Question
- [Backend] Ajout d'un champs `publish` (boolean) dans le modèle Question
- [Backend] Une ressource API `/questions/:id/stats` pour récupérer les résultats de chaque réponse
- [Frontend] Amélioration des champs meta dans le `<head>` de l'application, et ajout d'une image
- [Frontend] Le titre de la page (i.e. le nom de l'onglet) est maintenant un peu dynamique
- [Frontend] Ajout d'un favicon (i.e. le logo de l'onglet)
- [DevOps] Ajout du projet à [Kaffeine](https://kaffeine.herokuapp.com/) pour eviter que l'app backend se mette en pause (car elle tourne sur le plan gratuit Heroku)
- [Documentation] Ajout de la section `Idées` dans le README

### Modifié

- [Frontend] Meilleur affichage de la catégorie et de la difficulté des questions
- [Frontend] Ajout d'informations dans la page `/a-propos`

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
