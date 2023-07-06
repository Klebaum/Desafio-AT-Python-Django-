from django.urls import path
from . import views

urlpatterns = [
    path('indexView/', views.indexView, name='indexView'),
    path('', views.enviar_email, name='enviar_email'),
]