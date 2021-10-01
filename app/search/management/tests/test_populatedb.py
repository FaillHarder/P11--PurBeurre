from search.management.commands.populatedb import Command
from search.models import Product, Category

import json
import unittest
from unittest import mock


class TestCommand(unittest.TestCase):

    @mock.patch("search.management.commands.populatedb.Command.write_json_file_next_page")
    @mock.patch("search.management.commands.populatedb.Command.request_api_OFF")
    @mock.patch("search.management.commands.populatedb.Command.read_json_file")
    def test_handle(self, mock_read_json_file, mock_request_api_OFF, mock_write_json_file):

        mock_read_json_file.return_value = {
            "fields": [
                "product_name_fr"
            ],
            "categories": [
                "Snacks"
            ],
            "page": 1
        }

        mock_write_json_file.return_value = {
            "fields": [
                "product_name_fr"
            ],
            "categories": [
                "Snacks"
            ],
            "page": 2
        }

        mock_request_api_OFF.return_value = {
            "count": 22239,
            "page": 1,
            "page_count": 100,
            "page_size": 100,
            "products": [
                {
                    "carbohydrates_100g": 57.5,
                    "categories": "Spreads,Breakfasts,Sweet spreads,fr:Pâtes à tartiner,Hazelnut spreads,",
                    "energy-kcal_100g": 539,
                    "energy_100g": 2252,
                    "fat_100g": 30.9,
                    "fiber_100g": 0,
                    "id": "3017620422003",
                    "image_front_url": "https://images.openfoodfacts.org/images/products/front_fr.270.400.jpg",
                    "nutriscore_grade": "e",
                    "product_name_fr": "Nutella",
                    "proteins_100g": 6.3,
                    "salt_100g": 0.107,
                    "saturated-fat_100g": 10.6,
                    "sugars_100g": 56.3,
                    "url": "https://fr.openfoodfacts.org/produit/3017620422003/nutella-ferrero"
                },
                {
                    "carbohydrates_100g": 50.5,
                    "categories": "Spreads,Breakfasts,Sweet spreads,fr:Pâtes à tartiner,Hazelnut spreads,",
                    "energy-kcal_100g": 459,
                    "energy_100g": 6652,
                    "fat_100g": 80.9,
                    "fiber_100g": 0,
                    "id": "3017620422503",
                    "image_front_url": "https://images.openfoodfacts.org/images/products/front_fr.270.400.jpg",
                    "nutriscore_grade": "b",
                    "product_name_fr": "",
                    "proteins_100g": 7.2,
                    "salt_100g": 0.204,
                    "saturated-fat_100g": 12.7,
                    "sugars_100g": 63.7,
                    "url": "https://fr.openfoodfacts.org/produit/3017620422003/nutella-ferrero"
                }
            ]
        }

        cmd = Command()
        cmd.handle()
        self.assertTrue(mock_read_json_file.called)
        self.assertTrue(mock_request_api_OFF.called)
        self.assertTrue(mock_write_json_file.called)

    def test_read_json_file(self):
        mock_json_file = "search/management/tests/mock_settings.json"
        response = Command.read_json_file(self, mock_json_file)
        self.assertEqual(response["fields"][0], "product_name_fr")

    @mock.patch("search.management.commands.populatedb.Command.read_json_file")
    def test_write_json_file_next_page(self, mock_read_json_file):
        mock_read_json_file = {
            "fields": ["product_name_fr"],
            "categories": ["Snacks"],
            "page": 1
        }
        outfile = "search/management/tests/mock_settings2.json"
        Command.write_json_file_next_page(self, outfile, mock_read_json_file)
        with open(outfile, "r", encoding="utf-8") as file:
            result = json.load(file)
        self.assertEqual(result["page"], 2)

    def test_create_product(self):
        category = Category.objects.create(name="Snacks")
        data = {
                "product_name": "TestNutella",
                "bar_code": "3017620422003",
                "nutriscore": "e",
                "proteins_100g": 6.3,
                "energy_100g": 2252,
                "fat_100g": 30.9,
                "fiber_100g": 0,
                "carbohydrates_100g": 57.5,
                "salt_100g": 0.107,
                "saturated_fat_100g": 10.6,
                "sugars_100g": 56.3,
                "image": "https://images.openfoodfacts.org/front_fr.270.400.jpg",
                "url": "https://fr.openfoodfacts.org/produit/nutella-ferrero"
        }
        cmd = Command
        cmd.create_product(self, data, category)
        product = Product.objects.get(product_name="TestNutella")
        self.assertEqual(product.product_name, "TestNutella")
        self.assertEqual(category.name, "Snacks")
