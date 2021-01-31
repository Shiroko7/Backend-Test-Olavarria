import datetime
from django.test import TestCase, TransactionTestCase
from django.urls import reverse, resolve
from mealmngmt.models import Menu, MealManager, MenuRequest
from django.contrib.auth import get_user_model
from django.conf import settings

# Views that DON'T use model objects


class TestViews(TestCase):

    def setUp(self):
        pass

    def test_HomeView_get(self):
        response = self.client.get(reverse('home'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'mealmngmt/home.html')

# Views that use model objects


class TestTransactionView(TransactionTestCase):
    # setup dump database
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

    def test_MenuCreate_get(self):
        response = self.client.get(reverse('mealmngmt:create-menu'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'mealmngmt/create_menu.html')

    def test_MenuCreate_post(self):
        now = datetime.datetime.now()
        menu = Menu.objects.create(
            message='Menu test', date=now, mealmanager=self.nora)

        response = self.client.post(reverse('mealmngmt:create-menu'), {
            'message': 'Menu test',
            'date': now,
            'mealmanager': self.nora
        })
        self.assertEquals(response.status_code, 200)
        self.assertEquals(menu.message, 'Menu test')

    def test_MenuCreate_post_nodata(self):
        now = datetime.datetime.now()

        response = self.client.post(reverse('mealmngmt:create-menu'))
        self.assertEquals(response.status_code, 200)
        # only setup menu should be stored
        self.assertEquals(self.nora.menus.count(), 1)

    def test_MenuList_get(self):
        response = self.client.get(
            reverse('mealmngmt:menu-list'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'mealmngmt/menu_list.html')

    def test_MenuDetail_get(self):
        response = self.client.get(
            reverse('mealmngmt:menu-details', args=[self.menu.id]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'mealmngmt/menu_details.html')

    def test_MenuDetail_post(self):
        response = self.client.post(reverse('mealmngmt:menu-details', args=[self.menu.id]), {
            'initial_time': settings.OPEN_HOUR,
            'final_time': settings.CLOSE_HOUR,
            'interval': 60
        })
        self.assertEquals(response.status_code, 200)

    def test_MenuDetail_post_nodata(self):
        response = self.client.post(
            reverse('mealmngmt:menu-details', args=[self.menu.id]))
        self.assertEquals(response.status_code, 200)

    def test_MenuRequest_get(self):
        response = self.client.get(
            reverse('mealmngmt:menu', args=[self.menu.id]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'mealmngmt/menu.html')

    def test_MenuRequest_post(self):
        now = datetime.datetime.now()
        menurequest = MenuRequest.objects.create(first_name="testname1", last_name="testname2",
                                                 option="testoption", customization="testcustomization", menu=self.menu)

        response = self.client.post(reverse('mealmngmt:menu', args=[self.menu.id]), {
            'first_name': 'testname1',
            'last_name': 'testname2',
            'option': 'testoption',
            'customization': 'testcustomization',
            'menu': self.menu
        })
        self.assertEquals(response.status_code, 200)
        self.assertEquals(menurequest.first_name, 'testname1')

    def test_MenuCreate_post_nodata(self):
        now = datetime.datetime.now()

        response = self.client.post(
            reverse('mealmngmt:menu', args=[self.menu.id]))
        self.assertEquals(response.status_code, 200)
        # only setup menurequest should be stored
        self.assertEquals(self.menu.menurequests.count(), 1)
