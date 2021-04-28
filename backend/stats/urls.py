from django.urls import path

from stats import views


app_name = "stats"
urlpatterns = [
    # path("", views.api_home, name="index"),
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
    path("stats-dashboard", views.stats_dashboard, name="stats-dashboard"),
]
