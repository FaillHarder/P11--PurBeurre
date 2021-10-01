from search.models import Product

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Supprime les produits'

    def handle(self, *args, **options):
        Product.objects.all().delete()
