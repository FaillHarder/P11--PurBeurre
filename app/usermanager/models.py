from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    email = models.EmailField("Email", unique=True)
    username = models.CharField(null=True, max_length=30)
    # Login with email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('',)

    def get_absolute_url(self):
        return reverse('login')
