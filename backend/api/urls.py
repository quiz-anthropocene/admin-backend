from django.urls import path
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from api import views
from api.views import QuestionViewSet, QuizViewSet, CategoryViewSet, TagViewSet


app_name = "api"

router = routers.DefaultRouter()
router.register(r"questions", QuestionViewSet, basename="questions")
router.register(r"quizs", QuizViewSet, basename="quizs")
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"tags", TagViewSet, basename="tags")

urlpatterns = [
    path("", views.api_home, name="index"),
    # path("questions", views.question_list, name="question_list"),
    # path("questions/<int:pk>", views.question_detail, name="question_detail"),
    path("questions/random", views.question_random, name="question_random"),
    path("questions/count", views.question_count, name="question_count"),
    # path("categories", views.category_list, name="category_list"),
    # path("tags", views.tag_list, name="tag_list"),
    path("authors", views.author_list, name="author_list"),
    path(
        "difficulty-levels", views.difficulty_level_list, name="difficulty_level_list"
    ),
    # path("quizzes", views.quiz_list, name="quiz_list"),
    path("contribute", views.contribute, name="contribute_create"),
    path("glossary", views.glossary_list, name="glossary_list"),
    path("notion-questions", views.notion_questions, name="notion-questions"),
    path("newsletter", views.newsletter, name="newsletter"),
    # Swagger / OpenAPI documentation
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="api:schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="api:schema"), name="redoc"),
]

urlpatterns += router.urls
