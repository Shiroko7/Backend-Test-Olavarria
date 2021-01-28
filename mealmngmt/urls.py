from django.urls import path
from .views import create_menu, view_menu

app_name = "mealmngmt"

urlpatterns = [
    path('create-menu/', create_menu, name='create-menu'),
    path('menu/<uuid>/', view_menu, name='menu')
]
