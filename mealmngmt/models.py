import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


# Actors
class User(AbstractUser):
    pass


class MealManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

# Entities


class Menu(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.CharField(max_length=140)
    date = models.DateField()
    mealmanager = models.ForeignKey(
        MealManager, on_delete=models.CASCADE, related_name='menus')

    def __str__(self):
        return str(self.id)


class MenuRequest(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    option = models.CharField(max_length=40)
    customization = models.CharField(max_length=140)
    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE, related_name='menurequests')
