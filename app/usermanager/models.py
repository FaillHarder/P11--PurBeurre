from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):

    email = models.EmailField("Email", unique=True)
    username = models.CharField(null=True, max_length=30)
    # Login with email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('',)

    def get_absolute_url(self):
        return reverse('login')


class ImageProfile(models.Model):
    img_profile = models.ImageField(upload_to='avatar/')
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "{}".format(self.img_profile)
