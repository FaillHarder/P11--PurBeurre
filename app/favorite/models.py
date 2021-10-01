from search.models import Product
from django.conf import settings
from django.db import models


class Favorite(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    product_favorite = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_favorite.product_name

    def save_substitute(self, user, substitute):

        favorite = Favorite(user=user, product_favorite=substitute)
        favorite.save()
