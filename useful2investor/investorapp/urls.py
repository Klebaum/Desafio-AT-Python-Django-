from django.urls import path
from . import views

urlpatterns = [
    path("indexView/", views.indexView, name="indexView"),
    # path('', views.enviar_email, name='enviar_email'),
    # path('', views.salvar_email, name='salvar_email'),
    path("", views.show_stock_prices, name="show_stock_prices"),
]
