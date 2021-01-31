import datetime
from django.test import SimpleTestCase, TransactionTestCase
from django.urls import reverse, resolve
from mealmngmt.views import MenuCreateView, MenuListView, MenuDetailView,  MenuRequestView
from django.contrib.auth import get_user_model
from mealmngmt.models import Menu, MealManager


class TestSimpleUrls(SimpleTestCase):
    def test_CreateMenu_is_resolved(self):
        url = reverse('mealmngmt:create-menu')
        self.assertEquals(resolve(url).func.view_class, MenuCreateView)

    def test_MenuList_is_resolved(self):
        url = reverse('mealmngmt:menu-list')
        self.assertEquals(resolve(url).func.view_class, MenuListView)


class TestTransactionUrls(TransactionTestCase):
    # set up dump database
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user('Nora', password='1234')
        user.is_superuser = False
        user.is_staff = False
        user.save()

        nora = MealManager.objects.create(user=user)
        self.menu = Menu.objects.create(
            message="Menu test", date=datetime.datetime.now(), mealmanager=nora)

    def test_MenuDetail_is_resolved(self):
        url = reverse('mealmngmt:menu-details', args=[self.menu.id])
        self.assertEquals(resolve(url).func.view_class, MenuDetailView)

    def test_Menu_is_resolved(self):
        url = reverse('mealmngmt:menu', args=[self.menu.id])
        self.assertEquals(resolve(url).func.view_class, MenuRequestView)
