from django.urls import path
from .views import create_menu, menu_list, menu_details, view_menu

app_name = "mealmngmt"

urlpatterns = [
    path('create-menu/', create_menu, name='create-menu'),
    path('menu-list/', menu_list, name='menu-list'),
    path('menu-details/<uuid>/', menu_details, name='menu-details'),
    path('menu/<uuid>/', view_menu, name='menu')
]
