from django.urls import path
from api import views

app_name = "api"
urlpatterns = [
    path("", views.api_home, name="index"),
    path("questions", views.question_list, name="question_list"),
    path("questions/<int:pk>", views.question_detail, name="question_detail"),
    path("questions/<int:pk>/stats", views.question_stats, name="question_stats"),
    path(
        "questions/<int:pk>/feedback-events",
        views.question_detail_feedback_event,
        name="question_detail_feedback_event",
    ),
    path(
        "questions/<int:pk>/answer-events",
        views.question_detail_answer_event,
        name="question_detail_answer_event",
    ),
    path("questions/random", views.question_random, name="question_random"),
    path("questions/count", views.question_count, name="question_count"),
    path("categories", views.category_list, name="category_list"),
    path("tags", views.tag_list, name="tag_list"),
    path("authors", views.author_list, name="author_list"),
    path(
        "difficulty-levels", views.difficulty_level_list, name="difficulty_level_list"
    ),
    path("quizzes", views.quiz_list, name="quiz_list"),
    path(
        "quizzes/<int:pk>/feedback-events",
        views.quiz_detail_feedback_event,
        name="quiz_detail_feedback_event",
    ),
    path(
        "quizzes/<int:pk>/answer-events",
        views.quiz_detail_answer_event,
        name="quiz_detail_answer_event",
    ),
    path("contribute", views.contribute, name="contribute_create"),
    path("glossary", views.glossary_list, name="glossary_list"),
    path("stats", views.stats, name="stats"),
]
