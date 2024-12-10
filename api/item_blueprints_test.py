import unittest
from flask import Flask
from unittest.mock import patch
from api.item_blueprints import item_blueprint  # Adjust the import based on your project structure

class TestGetAllItems(unittest.TestCase):
    def setUp(self):
        # Create a Flask application instance for testing
        self.app = Flask(__name__)
        self.app.register_blueprint(item_blueprint)
        self.client = self.app.test_client()

    @patch('api.utils.helpers.retrieve_items_from_json')
    def test_get_all_items_success(self, mock_retrieve_items):
        # Arrange
        mock_items = \
            [
                {'description': 'Pink shirt', 'id': 0, 'price': 8},
                {'description': 'Red shirt', 'id': 1, 'price': 8},
                {'description': 'Purple shirt', 'id': 2, 'price': 8},
                {'description': 'Blue shirt', 'id': 3, 'price': 8},
                {'description': 'Black shirt', 'id': 4, 'price': 8}
            ]

        mock_retrieve_items.return_value = mock_items

        # Act
        response = self.client.get('/')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, mock_items)

if __name__ == '__main__':
    unittest.main()
