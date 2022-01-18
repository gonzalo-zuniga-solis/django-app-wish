from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('register', views.register),
    path('logout', views.logout),
    path('wish_items/create/', views.create),
    path('wish_items/delete/<int:id>', views.delete),
    path('item/preferencia/add/<int:id>', views.preferencias_add),
    path('item/preferencia/delete/<int:id>', views.preferencias_delete),
    ]
