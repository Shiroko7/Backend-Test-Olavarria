import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


# Actors
class User(AbstractUser):
    pass


class MealManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Employe(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=40)

# Entities


class Menu(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.CharField(max_length=140)
    date = models.DateField()
    mealmanager = models.ForeignKey(MealManager, on_delete=models.CASCADE)


class MenuRequest(models.Model):
    option = models.CharField(max_length=40),
    customization = models.CharField(max_length=140)
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)

# xoxb-1683708563844-1690268597857-XS6OkIBmsqCkQ3qeWAQKvabr
