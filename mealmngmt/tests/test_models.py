import datetime
from django.test import TestCase, TransactionTestCase
from django.urls import reverse, resolve
from mealmngmt.models import Menu, MealManager, MenuRequest
from django.contrib.auth import get_user_model


class TestModels(TestCase):
    # set up dump database
    # for the sake of this test it'll have 1 user named nora, 1 menu, and 1 request
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user('Nora', password='1234')
        user.is_superuser = False
        user.is_staff = False
        user.save()
        now = datetime.datetime.now()
        # meal manager nora logged in
        self.nora = MealManager.objects.create(user=user)
        self.logged_in = self.client.login(username='Nora', password='1234')
        # 1 menu created by nora
        self.menu = Menu.objects.create(
            message='Menu test', date=now, mealmanager=self.nora)
        # 1 request of said menu
        self.menurequest = MenuRequest.objects.create(first_name="testname1", last_name="testname2",
                                                      option="testoption", customization="testcustomization", menu=self.menu)

    def test_Menu(self):
        self.assertEquals(self.menu.message, 'Menu test')

    def test_MenuRequest(self):
        self.assertEquals(self.menurequest.first_name, 'testname1')
