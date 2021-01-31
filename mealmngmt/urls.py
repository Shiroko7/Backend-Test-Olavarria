from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import MenuCreateView, MenuListView,  MenuRequestView, MenuDetailView

app_name = "mealmngmt"

urlpatterns = [
    path('create-menu/', login_required(MenuCreateView.as_view()), name='create-menu'),
    path('menu-list/', login_required(MenuListView.as_view()), name='menu-list'),
    path('menu-details/<pk>/',
         login_required(MenuDetailView.as_view()), name='menu-details'),
    path('menu/<pk>/', MenuRequestView.as_view(), name='menu')
]
