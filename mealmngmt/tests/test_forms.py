import datetime
from django.test import SimpleTestCase
from mealmngmt.forms import SchedulerForm, CreateMenuModelForm, CreateMenuRequestModelForm
from mealmngmt.models import Menu, MealManager, MenuRequest
from django.contrib.auth import get_user_model
from django.conf import settings


class TestForms(SimpleTestCase):
    def test_SchedulerForm_valid(self):
        form = SchedulerForm(data={
            'initial_time': settings.OPEN_HOUR,
            'final_time': settings.CLOSE_HOUR,
            'interval': 60
        })
        self.assertTrue(form.is_valid())

    def test_SchedulerForm_NOTvalid(self):
        form = SchedulerForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)


class TestModelForms(SimpleTestCase):
    def setUp(self):
        self.now = datetime.datetime.now()

    def test_CreateMenuModelForm_valid(self):

        form = CreateMenuModelForm(data={
            'message': 'Menu test',
            'date': self.now
        })
        self.assertTrue(form.is_valid())

    def test_CreateMenuModelForm_NOTvalid(self):
        form = CreateMenuModelForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_CreateMenuRequestModelForm_valid(self):

        form = CreateMenuRequestModelForm(data={
            'first_name': 'testname1',
            'last_name': 'testname2',
            'option': 'testoption',
            'customization': 'testcustomization',
        })
        self.assertTrue(form.is_valid())

    def test_CreateMenuRequestModelForm_NOTvalid(self):
        form = CreateMenuRequestModelForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)
