# Changelog

Un suivi à jour des modifications apportées à ce projet (cf [Keep a Changelog](https://keepachangelog.com/en/1.0.0/))

Voir les [Issues](https://github.com/quiz-anthropocene/know-your-planet/issues) et le Board.

## [2.5.0](https://github.com/quiz-anthropocene/admin-backend/compare/v2.4.0...v2.5.0) (2024-02-20)

Setup release-please

## 2.4.0 (2023)

Interface contributeur
- Traductions

## 2.3.0 (2022-06)

Interface contributeur
- Pages "liste" : afficher les filtres actifs sous forme de badge
- Déplacé les actions administrateurs sous `/admin` (déplacé l'admin Django sous `/django`)
- Upload d'image (Questions & Quizs) et stockage sur S3-like

Automatisation
- Ajouter les nouveaux contributeurs à une liste Sendinblue

Autres
- Favicon
- Quelques résolutions de bugs

## 2.2.0 (2022-05)

Interface contributeur (v2)
- Historisation du contenu avec `django-simple-history` (Questions, Quizs, Glossaire), page avec les dernières modifications
- Pouvoir créer du contenu privé (Questions & Quizs), qui n'est pas exporté (ni visible dans l'API et les stats), modifiable seulement par l'auteur
- Glossaire : liste des termes, voir les détails d'un terme, créer, modifier
- Contributions : pouvoir changer le statut, pouvoir répondre
- Users : roles utilisateurs, règles métier en fonction du rôle
- Remplacer les Github Actions par le CRON de Scalingo
- Monitoring des erreurs

Code Github
- Transfert vers l'organisation `quiz-anthropocene`
- Split de la codebase `admin-backend` & `public-frontend`
- Exporter la donnée vers le Frontend seulement si il y a eu des changements sur le contenu publique

## 2.1.0 (2022-04)

Interface contributeur (v1)
- Header, Footer, Home, Breadcrumbs, pages d'erreur
- Page de connexion, réinitialisation du mot de passe
- Configuration email
- Questions : liste des questions (avec filtres), voir les détails d'une questions, créer, modifier, contributions, statistiques basiques
- Quizs : liste des quizs (avec filtres), voir les détails d'une questions, créer, modifier, contributions, statistiques basiques, liste des questions
- Tags : liste des tags, liste des questions concernées, liste des quizs concernés, créer un tag, modifier un tag
- Catégories : liste des catégories, liste des questions concernées, modifier une catégorie
- Contributions : liste des contributions. Lien entre le modèle et Question/Quiz.
- Users : page profil avec la liste de ses questions, de ses quizs. lien entre le modèle et Question/Quiz.

## 2.0.0 (2022-03)

Refonte de l'app Django
- Django v4
- Configuration : `flake8`, `black`, `isort`, `pre-commit`, `django-debug-toolbar`, `pyproject.toml`
- API : cleanup, utilisation de filtres (`django-filters`), documentation (`drf-spectacular`)
- Bouger les modèles dans leur propres apps, réinitialisation des migrations
- Nouveau modèle `User`
- Stats : nouveau modèle `QuizAggStat`. Ne plus supprimer `QuestionAnswerEvent` & `QuestionFeedbackEvent`. Perte de données des `QuizAnswerEvents` antérieurs à Mars 2022

## 1.3.0 (2021)

- [Data] Ajout du champ `slug` aux Quiz
- [Data] Compression des images PNG avec `pngquant`
- [DevOps] Utiliser `pipenv`
- [Backend] Bouger les stats dans leur propre app Django. Idem pour le modèle `Configuration`
- [Backend] Utiliser l'API officielle de Notion au lieu de `notion-py`
- [Backend] Stocker un `duration_seconds` pour chaque Quiz complété
- [Backend] Nouveaux champs `answer_audio`, `answer_video` & `answer_reading_recommendation` au modèle Question
- [Backend] Nouveaux champ `language` au modèle Quiz
- [Frontend] Ajout d'un module de traductions (i18n). Pouvoir switcher entre Français et Anglais.
- [Frontend] Nouveau logo
- [Frontend] Nouveau header fixe
- [Frontend] Mettre d'avantage de quizs en avant sur la home page
- [Frontend] Page dédié à l'atelier
- [Frontend] Améliorer l'expérience utilisateur (scroll, d'avantage de contenu sur la page...)
- [Frontend] Ajouter la license `by-nc-sa` dans le footer

## 1.2.0 (2020-12-13)

- [Data] Générer un fichier `data/stats.yaml` lors de l'export
- [Data] Générer un fichier `data/authors.yaml` lors de l'export (avec les `question_count` et `quiz_count`)
- [Data] Avoir les `question_count` dans le fichier `difficulty-levels.yaml`
- [DevOps] Migration du CI de CircleCI vers Github Actions
- [Backend] Stocker les erreurs d'import dans une Contribution
- [Backend] Export asynchrone des Contributions vers Notion
- [Backend] Les QCM-RM peuvent maintenant avoir qu'1 seule réponse
- [Frontend] Pouvoir accéder dans l'interface (via l'url) aux quizs non publiés
- [Frontend] Contribution: rajouter du texte pour proposer aux utilisateurs de laisser leur email

## 1.1.0 (2020-12-06)

- [Data] Nouveau dashboard Metabase connecté à la base de donnée de Scalingo
- [Backend] Nouveau modèle `Configuration` pour stocker des variables globales de l'application. Certains champs sont modifiables.
- [Backend] RichTextEditor pour les champs `introduction` & `conclusion` du modèle `Quiz` (pour pouvoir aller à la ligne)
- [Backend] Nouveau statut "Ecartée temporairement" pour les questions
- [Backend] Enlève le champ `publish` du modèle `Question` (on regarde maintenant seulement sont `validation_status`)
- [Backend] Créer les nouveaux tags automatiquement lors de l'import depuis Notion
- [Backend] Automatiser le lancement des tâches (import depuis Notion, export vers Github, aggrégation des Daily Stats) grâce à Github Actions
- [Backend] Exporter certains stats à chaque export de la donnée (pour éviter d'avoir un endpoint API et d'y faire des appels)
- [Frontend] Boutons de partage sur les réseaux sociaux à la fin d'un quiz

## 1.0.0 (2020-11-29)

- [Data] Ajout d'images de laydgeur
- [Data] Ajout de Bon Pote dans les soutiens
- [DevOps] Migration du backend de Heroku vers Scalingo
- [Backend] Ajout d'un champ `question_count` dans le modèle `QuizAnswerEvent` (pour garder des stats de réussites claires même si le nombre de questions du quiz change)
- [Backend] Toujours mettre `publish=True` lors de l'import si la question est Validée (bug fix)
- [Frontend] Afficher les 3 derniers quizs sur la page d'accueil
- [Frontend] Ajout des filtres sur la page des quizs

## TODO

## 0.7.0

### Ajouté

- [Admin] Graph affichant le nombre de réponses aux quizs par jour
- [DevOps] Linting automatique du code backend avec `flake8`, `black` et un pre-commit git hook
- [DevOps] Ajout d'un fichier `CONTRIBUTING.md`

### Modifié

- [Backend] Renommé le modèle `QuestionCategory` en `Category`
- [Backend] Renommé le modèle `QuestionTag` en `Tag`

## 0.6.0 (2020-04-17)

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

## 0.5.0 (2020-04-05)

### Ajouté

- [Admin] Fonctions d'export de la donnée (csv, json, yaml)
- [Admin] Graph affichant le nombre de réponses par jour
- [Backend] Un modèle `QuestionCategory` pour stocker les catégories (au lieu d'un champ)
- [Backend] Un modèle `QuestionTag` pour stocker les tags

### Modifié

- [Backend] Le champ catégorie passe d'un CharField à une ForeignKey
- [Backend] Utilisation de URLField pour les champ url de `Question`
- [Frontend] Rajout d'une action 'commentaire' sur la page de contribution

## 0.4.0 (2020-03-27)

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

## 0.3.0 (2020-03-22)

### Ajouté

- [Backend] Ajout d'un champs `answer_image_link` dans le modèle Question
- [Frontend] Une page Stats pour afficher quelques les chiffres basiques de l'application (nombre de questions, nombre de réponses, ...)
- [Frontend] Un bouton "Autre question dans la même catégorie"
- [Frontend] Affiche l'auteur et les statistiques de la question (dans la réponse)

### Modifié

- [DevOps] Ajout de la commande loaddata au Procfile
- [Frontend] Typo dans la description de l'application

## 0.2.0 (2020-03-11)

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

## 0.1.0 (2020-03-08)

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
