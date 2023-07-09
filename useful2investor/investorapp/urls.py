from django.urls import path
from . import views

urlpatterns = [
    path("indexView/", views.save_values, name="save_values"),
    path("", views.send_email, name="send_email"),
    path("show_asset_info/<str:email>/", views.show_asset_info, name="show_asset_info"),
    path('remove_assets/<str:email>/', views.remove_assets, name='remove_assets'),
    path('add_assets/<str:email>/', views.add_assets, name='add_assets'),
]
