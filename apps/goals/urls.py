from django.urls import path
from django.contrib.auth import views
from . import views

urlpatterns = [

    path('', views.goals_page, name="goals_page"),
    path('create/', views.create_goal, name="create_goal"),
    path('form/<str:pk>/', views.update_goal, name="goal_form"),
    path('complete/<str:pk>/', views.complete_goal, name="complete_goal"),
    path('delete/<str:pk>/', views.delete_goal, name="delete_goal"),

]