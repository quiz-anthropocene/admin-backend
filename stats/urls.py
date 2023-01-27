from rest_framework import routers

from stats.views import (
    LinkClickEventViewSet,
    QuestionAnswerEventViewSet,
    QuestionFeedbackEventViewSet,
    QuizAnswerEventViewSet,
    QuizFeedbackEventViewSet,
)


app_name = "stats"

router = routers.DefaultRouter()
router.register(r"question-answer-event", QuestionAnswerEventViewSet, basename="question-answer-event")
router.register(r"question-feedback-event", QuestionFeedbackEventViewSet, basename="question-feedback-event")
router.register(r"quiz-answer-event", QuizAnswerEventViewSet, basename="quiz-answer-event")
router.register(r"quiz-feedback-event", QuizFeedbackEventViewSet, basename="quiz-feedback-event")
router.register(r"link-click-event", LinkClickEventViewSet, basename="link-click-event")

urlpatterns = []

urlpatterns += router.urls
