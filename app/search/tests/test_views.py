from search.views import index, search_product, substitute, mentions
from search.models import Product, Category

from django.test import RequestFactory, TestCase


class TestView(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.category = Category.objects.create(name="Snacks sucrés")
        self.product = Product.objects.create(
            product_name="nutella",
            bar_code="3017620425035",
            nutriscore="e",
            proteins_100g="6.3",
            energy_100g="2252.00",
            fat_100g="30.90",
            fiber_100g="0.00",
            carbohydrates_100g="57.50",
            salt_100g="0.11",
            saturated_fat_100g="10.60",
            sugars_100g="56.30",
            image="https://static.openfoodfacts.org/images/products/301/762/042/5035/front_fr.315.400.jpg",
            url="https://fr.openfoodfacts.org/produit/3017620425035/nutella-ferrero"
        )
        self.product.categories.add(self.category)
        return super().setUp()

    def test_index(self):
        request = self.factory.get("")
        view = index(request)
        self.assertEqual(view.status_code, 200)

    def test_search_product(self):
        request = self.factory.get("/search_product")
        request.GET = {"query": ""}
        view = search_product(request)
        self.assertEqual(view.status_code, 302)
        request.POST = {"query": "nutella"}
        view = search_product(request)
        self.assertEqual(view.status_code, 302)

        request.GET = {"query": "nutella"}
        view = search_product(request)
        self.assertEqual(view.status_code, 200)
        self.assertEqual(str(self.product), "nutella")
        self.assertEqual(str(self.category), "Snacks sucrés")

        request.GET = {"query": "pain"}
        view = search_product(request)
        self.assertEqual(view.status_code, 200)

    def test_substitute(self):
        request = self.factory.get("/substitute", {"query": "3017620425035"})
        view = substitute(request)
        self.assertEqual(view.status_code, 200)

    def test_mentions(self):
        request = self.factory.get("/mentions")
        view = mentions(request)
        self.assertEqual(view.status_code, 200)
