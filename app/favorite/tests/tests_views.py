from search.models import Product, Category
from favorite.models import Favorite
from favorite.views import product_save, myfood, description

from usermanager.models import User
from django.test import RequestFactory, TestCase


# Create your tests here.
class ViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="usernametest",
            first_name="firstnametest",
            last_name="lastnametest",
            email="email@test.fr",
            password="passwordtest"
        )
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
        self.favorite = Favorite(user=self.user, product_favorite=self.product)

        return super().setUp()

    def test_product_save(self):
        request = self.factory.get(
            'product_save',
            {"substitute": "3017620425035"}
        )
        request.user = self.user
        view = product_save(request)
        self.assertEqual(view.status_code, 200)
        self.assertEqual(str(self.favorite), "nutella")

    def test_myfood(self):
        request = self.factory.get("myfood")
        request.user = self.user
        view = myfood(request)
        self.assertEqual(view.status_code, 200)

    def test_description(self):
        request = self.factory.get(
            "description",
            {"query": "3017620425035"}
        )
        request.user = self.user
        view = description(request)
        self.assertEqual(view.status_code, 200)
