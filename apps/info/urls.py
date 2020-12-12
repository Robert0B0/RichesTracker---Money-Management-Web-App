from django.urls import path
from django.contrib.auth import views
from . import views

urlpatterns = [

    path('calendar/', views.calendar_page, name="calendar_page"),
    path('graph/', views.graph_page, name="graph_page"),

]