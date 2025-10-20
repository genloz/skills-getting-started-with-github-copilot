"""
Tests for static file serving and general app functionality.
"""

import pytest
from fastapi.testclient import TestClient


class TestStaticFiles:
    """Test class for static file serving and app functionality."""

    def test_static_html_file_accessible(self, client):
        """Test that static HTML files are accessible."""
        response = client.get("/static/index.html")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")

    def test_static_css_file_accessible(self, client):
        """Test that static CSS files are accessible."""
        response = client.get("/static/styles.css")
        assert response.status_code == 200
        assert "text/css" in response.headers.get("content-type", "")

    def test_static_js_file_accessible(self, client):
        """Test that static JavaScript files are accessible."""
        response = client.get("/static/app.js")
        assert response.status_code == 200
        # JavaScript might be served as text/javascript or application/javascript
        content_type = response.headers.get("content-type", "")
        assert any(js_type in content_type for js_type in ["javascript", "text/plain"])

    def test_nonexistent_static_file(self, client):
        """Test that nonexistent static files return 404."""
        response = client.get("/static/nonexistent.html")
        assert response.status_code == 404

    def test_app_title_and_description(self, client):
        """Test that the app has correct title and description from FastAPI."""
        # This tests the OpenAPI docs endpoint
        response = client.get("/docs")
        assert response.status_code == 200
        
        # Test the OpenAPI schema
        openapi_response = client.get("/openapi.json")
        assert openapi_response.status_code == 200
        
        schema = openapi_response.json()
        assert schema["info"]["title"] == "Mergington High School API"
        assert "extracurricular activities" in schema["info"]["description"]


class TestAPIEndpoints:
    """Test class for general API endpoint behavior."""

    def test_cors_headers_not_present_by_default(self, client, reset_activities):
        """Test that CORS headers are not present by default."""
        response = client.get("/activities")
        assert response.status_code == 200
        # CORS headers should not be present unless explicitly configured
        assert "access-control-allow-origin" not in response.headers

    def test_api_returns_json_content_type(self, client, reset_activities):
        """Test that API endpoints return JSON content type."""
        response = client.get("/activities")
        assert response.status_code == 200
        assert "application/json" in response.headers.get("content-type", "")

    def test_signup_post_method_only(self, client, reset_activities):
        """Test that signup endpoint only accepts POST method."""
        # POST should work
        response = client.post(
            "/activities/Chess Club/signup?email=test@mergington.edu"
        )
        assert response.status_code == 200
        
        # GET should not work
        response = client.get(
            "/activities/Chess Club/signup?email=test@mergington.edu"
        )
        assert response.status_code == 405  # Method Not Allowed

    def test_unregister_delete_method_only(self, client, reset_activities):
        """Test that unregister endpoint only accepts DELETE method."""
        # First sign up a participant
        client.post("/activities/Chess Club/signup?email=test@mergington.edu")
        
        # DELETE should work
        response = client.delete(
            "/activities/Chess Club/unregister?email=test@mergington.edu"
        )
        assert response.status_code == 200
        
        # POST should not work
        response = client.post(
            "/activities/Chess Club/unregister?email=test@mergington.edu"
        )
        assert response.status_code == 405  # Method Not Allowed