from django.db import models
from django.db.models import Count


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_name = models.CharField(max_length=200)
    bar_code = models.CharField(max_length=20, primary_key=True)
    nutriscore = models.CharField(max_length=2)
    proteins_100g = models.DecimalField(max_digits=7, decimal_places=2)
    energy_100g = models.DecimalField(max_digits=7, decimal_places=2)
    fat_100g = models.DecimalField(max_digits=7, decimal_places=2)
    fiber_100g = models.DecimalField(max_digits=7, decimal_places=2)
    carbohydrates_100g = models.DecimalField(max_digits=7, decimal_places=2)
    salt_100g = models.DecimalField(max_digits=7, decimal_places=2)
    saturated_fat_100g = models.DecimalField(max_digits=7, decimal_places=2)
    sugars_100g = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.TextField()
    url = models.TextField()
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.product_name

    def search(self, query):
        """Method taking user input as parameter.
           Find the products corresponding to the user's request.
           Retrun a list of 6 products"""
        product_search = Product.objects.filter(
            product_name__icontains=query
        )[:6]
        return product_search

    def substitute(self, query):
        """Method taking as parameter the bar code of the selected product.
           Returns a list of 6 substitutes sorted by nutriscore"""
        product = Product.objects.get(bar_code=query)
        # sort the categories by the increasing number of products
        category_by_number_products = Category.objects.annotate(
            num_products=Count("product")
            ).order_by("num_products")
        better_category = category_by_number_products.filter(product=product)

        sub_products = Product.objects.filter(
            nutriscore__lte=product.nutriscore,
            categories=better_category[0]
        ).order_by('nutriscore')[:3]
        return sub_products
