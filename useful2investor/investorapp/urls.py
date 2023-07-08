from django.urls import path
from . import views

urlpatterns = [
    path("indexView/", views.indexView, name="indexView"),
    path("", views.save_email_assets, name="save_email_assets"),
    path("", views.send_email, name="send_email"),
    path("stock_price/<str:email>/", views.show_stock_prices, name="show_stock_prices"),
]
