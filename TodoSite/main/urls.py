from django.urls import path
from . import views

urlpatterns = [

    path('', views.tables, name='home'),
    path('create_task/', views.create_task, name="create_task"),
    path('create_comment/', views.create_comment, name="create_comment"),

]