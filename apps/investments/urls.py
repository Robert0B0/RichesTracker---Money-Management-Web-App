from django.urls import path
from django.contrib.auth import views
from . import views

urlpatterns = [

    path('', views.investments_page, name="investments_page"),
    path('create/', views.investment_create, name="create_investment"),
    path('form/<str:pk>/', views.investment_update, name="investment_form"),
    path('delete/<str:pk>/', views.investment_delete, name="delete_investment"),
    path('invest/<str:pk>/', views.investment_invest, name="invest_investment"),
    path('invest_all/', views.investment_invest_all, name="invest_all_investment"),
    path('cash_out/<str:pk>/', views.investment_cash_out, name="cash-out_investment"),


]