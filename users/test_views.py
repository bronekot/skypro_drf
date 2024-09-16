import stripe
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class StripeIntegrationTests(APITestCase):
    def setUp(self):
        self.product_url = reverse("api-users:create-product")
        self.price_url = reverse("api-users:create-price")
        self.session_url = reverse("api-users:create-checkout-session")
        self.product_data = {
            "name": "Test Product",
            "description": "This is a test product",
        }
        self.price_data = {
            "product_id": "",  # This will be set after creating a product
            "unit_amount": 2000,
            "currency": "usd",
        }
        self.session_data = {
            "price_id": "",  # This will be set after creating a price
            "success_url": "https://example.com/success",
            "cancel_url": "https://example.com/cancel",
        }

    def test_create_product(self):
        response = self.client.post(self.product_url, self.product_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.price_data["product_id"] = response.data["id"]

    def test_create_price(self):
        # First, create a product
        product_response = self.client.post(
            self.product_url, self.product_data, format="json"
        )
        self.price_data["product_id"] = product_response.data["id"]

        # Then, create a price
        response = self.client.post(self.price_url, self.price_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.session_data["price_id"] = response.data["id"]

    def test_create_checkout_session(self):
        # First, create a product
        product_response = self.client.post(
            self.product_url, self.product_data, format="json"
        )
        self.price_data["product_id"] = product_response.data["id"]

        # Then, create a price
        price_response = self.client.post(
            self.price_url, self.price_data, format="json"
        )
        self.session_data["price_id"] = price_response.data["id"]

        # Finally, create a checkout session
        response = self.client.post(self.session_url, self.session_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
