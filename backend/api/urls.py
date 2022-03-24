from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework import routers

from api import views
from api.views import (
    CategoryViewSet,
    ContributionViewSet,
    GlossaryViewSet,
    QuestionDifficultyViewSet,
    QuestionLanguageViewSet,
    QuestionTypeViewSet,
    QuestionValidationStatusViewSet,
    QuestionViewSet,
    QuizViewSet,
    TagViewSet,
)


app_name = "api"

router = routers.DefaultRouter()
router.register(r"questions/types", QuestionTypeViewSet, basename="question-type")
router.register(r"questions/difficulties", QuestionDifficultyViewSet, basename="question-difficulty")
router.register(r"questions/languages", QuestionLanguageViewSet, basename="question-language")
router.register(
    r"questions/validation-status", QuestionValidationStatusViewSet, basename="question-validation-status"
)  # noqa
router.register(r"questions", QuestionViewSet, basename="question")
router.register(r"quizs", QuizViewSet, basename="quiz")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"tags", TagViewSet, basename="tag")
router.register(r"glossary", GlossaryViewSet, basename="glossary")
router.register(r"contribution", ContributionViewSet, basename="contribution")

urlpatterns = [
    path("", views.api_home, name="index"),
    # path("questions/random", views.question_random, name="question_random"),
    # path("authors", views.author_list, name="author_list"),
    # path("notion-questions", views.notion_questions, name="notion-questions"),
    path("newsletter", views.newsletter, name="newsletter"),
    # Swagger / OpenAPI documentation
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="api:schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="api:schema"), name="redoc"),
]

urlpatterns += router.urls
