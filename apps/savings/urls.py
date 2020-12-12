from django.urls import path
from django.contrib.auth import views
from . import views


urlpatterns = [

    path('', views.savings_page, name="savings_page"),
    path('create/', views.create_saving, name="create_savings"),
    path('form/<str:pk>/', views.update_saving, name="savings_form"),
    path('break/<str:pk>/', views.break_saving, name="break_savings"),
    path('delete/<str:pk>/', views.delete_saving, name="delete_savings"),
    path('tip/<str:pk>/', views.tip_saving, name="saving_tip"),
    path('savings_tip/', views.tip_all_savings, name='tip_all_savings'),

]