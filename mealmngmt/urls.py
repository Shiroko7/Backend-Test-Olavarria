from django.urls import path
from .views import create_menu

app_name = "mealmngmt"

urlpatterns = [
    path('create-menu', create_menu)
]
