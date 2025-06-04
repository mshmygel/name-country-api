from unittest.mock import patch
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class NamePredictionViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        self.url = reverse("name-prediction")
        self.valid_name = "michael"

    @patch("names.views.get_country_details")
    @patch("names.views.get_nationalize_data")
    def test_prediction_with_valid_name(self, mock_get_nationalize, mock_get_country):
        """
        Should return 200 OK with mocked country predictions for a valid name.
        """
        mock_get_nationalize.return_value = [{"country_id": "US", "probability": 0.9}]
        mock_get_country.return_value = {
            "name": {
                "official": "United States of America",
                "common": "United States"
            },
            "region": "Americas",
            "subregion": "North America",
            "capital": ["Washington, D.C."],
            "latlng": [38.0, -97.0],
            "flags": {
                "png": "https://example.com/flag.png",
                "svg": "https://example.com/flag.svg"
            },
            "coatOfArms": {
                "png": "",
                "svg": ""
            },
            "borders": ["CAN", "MEX"],
            "independent": True
        }

        response = self.client.get(self.url, {"name": self.valid_name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("name", response.data)
        self.assertIn("country_probabilities", response.data)
        self.assertIsInstance(response.data["country_probabilities"], list)

    def test_prediction_without_name(self):
        """
        Should return 400 Bad Request if name is missing.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_prediction_without_authentication(self):
        """
        Should return 401 Unauthorized if token is missing.
        """
        self.client.credentials()  # Remove token
        response = self.client.get(self.url, {"name": self.valid_name})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_prediction_with_invalid_token(self):
        """
        Should return 401 Unauthorized if token is invalid.
        """
        self.client.credentials(HTTP_AUTHORIZATION="Bearer invalid.token")
        response = self.client.get(self.url, {"name": self.valid_name})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
