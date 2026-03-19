"""
Script Name : views.py
Description : Core API views for root and health endpoints
Author : @tonybnya
"""

import os

from django.db import connection
from django.db.utils import OperationalError
from rest_framework.views import APIView
from rest_framework.response import Response


class APIInfoView(APIView):
    """Return API information at root endpoint."""

    def get(self, request):
        """Return API info (name, version, status)."""
        return Response(
            {
                "name": "Echoo API",
                "version": "1.0.0",
                "status": "running",
                "url": "https://echoo-api.onrender.com",
            }
        )


class HealthCheckView(APIView):
    """Health check endpoint with database connectivity status."""

    def get(self, request):
        """Check database connectivity and return health status."""
        database_url = os.environ.get("DATABASE_URL", "Not configured")
        db_type = "unknown"

        if database_url.startswith("postgresql://"):
            db_type = "postgresql"
        elif database_url.startswith("sqlite://"):
            db_type = "sqlite"

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            database_status = "connected"
            overall_status = "healthy"
        except OperationalError as e:
            database_status = f"disconnected: {str(e)}"
            overall_status = "unhealthy"
        except Exception as e:
            database_status = f"error: {str(e)}"
            overall_status = "unhealthy"

        return Response(
            {
                "status": overall_status,
                "database": {
                    "type": db_type,
                    "status": database_status,
                    "configured": database_url != "Not configured",
                },
            }
        )
