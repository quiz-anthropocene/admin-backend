from django.urls import path
from api import views

app_name = "api"
urlpatterns = [
    path("", views.api_home, name="index"),
    path("questions/", views.question_list, name="question_list"),
    path("questions/<int:pk>/", views.question_detail, name="question_detail"),
    path(
        "questions/<int:pk>/stats",
        views.question_detail_stats,
        name="question_detail_stats",
    ),
    path("questions/random", views.question_random, name="question_random"),
    path("questions/count", views.question_count, name="question_count"),
    path("categories", views.category_list, name="category_list"),
    path("tags", views.tag_list, name="tag_list"),
    path("authors", views.author_list, name="author_list"),
    path("difficulty-levels", views.difficulty_list, name="difficulty_level_list"),
    path("quizzes", views.quiz_list, name="quiz_list"),
    path("quizzes/<int:pk>/stats", views.quiz_detail_stats, name="quiz_detail_stats"),
    path("contribute", views.contribute, name="contribute_create"),
    path("stats", views.stats, name="stats"),
]
