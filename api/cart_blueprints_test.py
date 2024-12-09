import unittest
from flask import Flask
from api.utils.helpers import retrieve_items_from_json
from api.utils.types import CartList, Cart, ShirtList
from api.cart_blueprints import cart_blueprint, calculate_cart_total_price  # Replace 'your_module' with the actual module name

class CartTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(cart_blueprint)
        self.client = self.app.test_client()

        # Mock the items to avoid dependency on external JSON
        self.mock_items = [
            {"id": 0, "price": 10.0},
            {"id": 1, "price": 20.0},
            {"id": 2, "price": 30.0},
            {"id": 3, "price": 40.0},
            {"id": 4, "price": 50.0},
            {"id": 5, "price": 60.0},
        ]

        # Mock the retrieve_items_from_json function
        def mock_retrieve_items_from_json():
            return self.mock_items

        # Replace the original function with the mock
        retrieve_items_from_json = mock_retrieve_items_from_json

    def test_calculate_cart_total_price_no_items(self):
        cart: CartList = []
        total_price = calculate_cart_total_price(cart)
        self.assertEqual(total_price, 0.0)

    def test_calculate_cart_total_price_with_discount(self):
        cart: CartList = [
            {"id": 0, "quantity": 1},
            {"id": 1, "quantity": 1},
            {"id": 2, "quantity": 1},
            {"id": 3, "quantity": 1},
            {"id": 4, "quantity": 1},  # Ensure this ID exists in mock
        ]
        total_price = calculate_cart_total_price(cart)
        self.assertAlmostEqual(total_price, 40 * 0.8)  # Verify if mock data and logic cover this correctly

    def test_add_to_cart_item_not_found(self):
        response = self.client.put('/update', json={
            "cart": [],
            "cartItem": {"id": 999, "quantity": 1}  # Non-existent item
        })
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {"message": "Item not found"})

    def test_add_to_cart_item_found(self):
        response = self.client.put('/update', json={
            "cart": [],
            "cartItem": {"id": 1, "quantity": 1}  # Existing item
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("cart", response.json)
        self.assertEqual(len(response.json["cart"]), 1)
        self.assertEqual(response.json["cart"][0]["id"], 1)
        self.assertEqual(response.json["cart"][0]["quantity"], 1)

    def test_add_to_cart_item_already_in_cart(self):
        response = self.client.put('/update', json={
            "cart": [{"id": 1, "quantity": 1}],
            "cartItem": {"id": 1, "quantity": 2}  # Existing item, increase quantity
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("cart", response.json)
        self.assertEqual(len(response.json["cart"]), 1)
        self.assertEqual(response.json["cart"][0]["quantity"], 3)  # Quantity should be updated

if __name__ == '__main__':
    unittest.main()
