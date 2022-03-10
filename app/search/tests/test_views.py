from search.views import index, search_product, substitute, mentions, ajax_search_product
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
        self.product_2 = Product.objects.create(
            product_name="Pate à tartiner",
            bar_code="3700477609504",
            nutriscore="d",
            proteins_100g="6",
            energy_100g="2311.00",
            fat_100g="24.00",
            fiber_100g="0.00",
            carbohydrates_100g="53.00",
            salt_100g="0",
            saturated_fat_100g="6.00",
            sugars_100g="52.00",
            image="https://images.openfoodfacts.org/images/products/370/047/760/9504/front_fr.53.400.jpg",
            url="https://fr.openfoodfacts.org/produit/3700477609504/pate-a-tartiner-chocolat"
        )
        self.product_2.categories.add(self.category)
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
        # requet post redirect index
        request = self.factory.post("/search_product")
        view = search_product(request)
        self.assertEqual(view.status_code, 302)

    def test_substitute(self):
        request = self.factory.get("/substitute", {"query": "3017620425035"})
        view = substitute(request)
        self.assertEqual(view.status_code, 200)
        # return a substitute with the nutriscore less than or equal to that of nutella
        substitute_result = Product().substitute("3017620425035")
        self.assertEqual(len(substitute_result), 2)

    def test_mentions(self):
        request = self.factory.get("/mentions")
        view = mentions(request)
        self.assertEqual(view.status_code, 200)

    def test_ajax_search_product(self):
        request = self.factory.post("ajax_search_product", {"query": "nutella"})
        view = ajax_search_product(request)
        self.assertEqual(view.status_code, 200)

        request = self.factory.post("ajax_search_product", {"query": ""})
        view = ajax_search_product(request)
        self.assertEqual(view.status_code, 200)
