import unittest
from flask import Flask
from flask.testing import FlaskClient
from server import app  # Ensure this imports the app from your script


class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        # Create a test client for the Flask application
        self.app = app
        self.client: FlaskClient = app.test_client()
        self.app.testing = True

    def test_blueprints_registered(self):
        # Verify that the blueprints are registered
        self.assertIn('item_blueprint', self.app.blueprints)
        self.assertIn('cart_blueprint', self.app.blueprints)

    def test_cors_settings(self):
        # Verify CORS headers are set correctly
        response = self.client.get('/')
        self.assertEqual(response.headers.get('Access-Control-Allow-Origin'), '*')


if __name__ == '__main__':
    unittest.main()
