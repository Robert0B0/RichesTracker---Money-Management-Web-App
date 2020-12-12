from django.urls import path
from django.contrib.auth import views
from . import views


urlpatterns = [

    path('login/', views.login_page, name="login_page"),
    path('register/', views.register_page, name="register_page"),
    path('logout/', views.logout_user, name="logout"),
    path('setting/', views.settings_page, name="user-settings"),
    path('', views.home_page, name="home"),

    
    path('about/', views.about_page, name="about"),
    path('bugs/', views.bugs_page, name="bugs"),

]