from django.urls import path
from api import views


urlpatterns = [
    path('', views.api_home),
    path('questions/', views.question_list),
    path('questions/<int:pk>/', views.question_detail),
    path('questions/<int:pk>/stats', views.question_detail_stats),
    path('questions/random', views.question_random),
    path('questions/stats', views.question_stats),
    path('categories', views.category_list),
]
