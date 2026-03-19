"""
Script Name : tests.py
Description : Tests for core API endpoints
Author : @tonybnya
"""

from django.test import TestCase
from rest_framework.test import APIClient


class CoreAPIViewsTest(TestCase):
    """Test cases for core API endpoints."""

    def setUp(self):
        self.client = APIClient()

    def test_api_info_endpoint(self):
        """Test GET / returns API info."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "Echoo API")
        self.assertEqual(data["version"], "1.0.0")
        self.assertEqual(data["status"], "running")

    def test_health_check_endpoint(self):
        """Test GET /health returns health status."""
        response = self.client.get("/health/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("database", data)
        self.assertIn("status", data["database"])
        self.assertIn("type", data["database"])
        self.assertIn("configured", data["database"])
