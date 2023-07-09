from django.urls import path
from . import views

urlpatterns = [
    path("indexView/", views.save_values, name="save_values"),
    #path("", views.save_email_assets, name="save_email_assets"),
    path("", views.send_email, name="send_email"),
    path("show_asset_info/<str:email>/", views.show_asset_info, name="show_asset_info"),
    #path("stock_prices", views.show_values, name="show_values"),
    #path("stock_price/<str:email>/<str:minutes>/", views.show_stock_prices, name="show_stock_prices"),
]
