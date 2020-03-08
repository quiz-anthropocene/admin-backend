from django.urls import path
from api import views


urlpatterns = [
    path('', views.api_home),
    path('questions/', views.question_list),
    path('questions/<int:pk>/', views.question_detail),
    path('questions/random', views.question_random),
]
