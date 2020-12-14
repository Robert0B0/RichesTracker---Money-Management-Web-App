from django.urls import path
from django.contrib.auth import views
from . import views

urlpatterns = [

    path('', views.record_page, name="record_page"),
    path('create/', views.create_record, name="create_record"),
    path('form/<str:pk>/', views.update_record, name="record_form"),
    path('delete/<str:pk>/', views.delete_record, name="delete_record"),


    path('create/', views.create_record_modal, name="add_record"),
    path('update/', views.update_record_modal, name="update_record"),
    

]