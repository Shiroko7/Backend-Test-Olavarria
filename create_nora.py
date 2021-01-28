from django.contrib.auth import get_user_model
from mealmngmt.models import MealManager

User = get_user_model()

if not User.objects.filter(username='Nora').exists():
    user = User.objects.create_user('Nora', password='1234')
    user.is_superuser = False
    user.is_staff = False
    user.save()

    MealManager.objects.create(user=user)
