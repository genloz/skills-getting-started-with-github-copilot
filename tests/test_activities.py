"""
Tests for the FastAPI activities endpoints.
"""

import pytest
from fastapi.testclient import TestClient


class TestActivitiesAPI:
    """Test class for activities API endpoints."""

    def test_root_redirect(self, client):
        """Test that root endpoint redirects to static/index.html."""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert "static/index.html" in response.headers["location"]

    def test_get_activities(self, client, reset_activities):
        """Test getting all activities."""
        response = client.get("/activities")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 9  # We have 9 activities in the initial data
        
        # Check that Chess Club exists with correct structure
        assert "Chess Club" in data
        chess_club = data["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert chess_club["max_participants"] == 12
        assert "michael@mergington.edu" in chess_club["participants"]

    def test_signup_for_activity_success(self, client, reset_activities):
        """Test successful signup for an activity."""
        response = client.post(
            "/activities/Chess Club/signup?email=newstudent@mergington.edu"
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["message"] == "Signed up newstudent@mergington.edu for Chess Club"
        
        # Verify the participant was added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]

    def test_signup_for_nonexistent_activity(self, client, reset_activities):
        """Test signup for an activity that doesn't exist."""
        response = client.post(
            "/activities/Nonexistent Club/signup?email=student@mergington.edu"
        )
        assert response.status_code == 404
        
        data = response.json()
        assert data["detail"] == "Activity not found"

    def test_signup_duplicate_participant(self, client, reset_activities):
        """Test signup when student is already registered."""
        # michael@mergington.edu is already in Chess Club
        response = client.post(
            "/activities/Chess Club/signup?email=michael@mergington.edu"
        )
        assert response.status_code == 400
        
        data = response.json()
        assert data["detail"] == "Student is already signed up for this activity"

    def test_unregister_from_activity_success(self, client, reset_activities):
        """Test successful unregistration from an activity."""
        response = client.delete(
            "/activities/Chess Club/unregister?email=michael@mergington.edu"
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["message"] == "Unregistered michael@mergington.edu from Chess Club"
        
        # Verify the participant was removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]

    def test_unregister_from_nonexistent_activity(self, client, reset_activities):
        """Test unregistration from an activity that doesn't exist."""
        response = client.delete(
            "/activities/Nonexistent Club/unregister?email=student@mergington.edu"
        )
        assert response.status_code == 404
        
        data = response.json()
        assert data["detail"] == "Activity not found"

    def test_unregister_non_participant(self, client, reset_activities):
        """Test unregistration when student is not registered."""
        response = client.delete(
            "/activities/Chess Club/unregister?email=nonparticipant@mergington.edu"
        )
        assert response.status_code == 400
        
        data = response.json()
        assert data["detail"] == "Student is not registered for this activity"

    def test_signup_and_unregister_workflow(self, client, reset_activities):
        """Test complete workflow of signup followed by unregistration."""
        email = "testworkflow@mergington.edu"
        activity = "Programming Class"
        
        # First, sign up
        signup_response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        assert signup_response.status_code == 200
        
        # Verify signup
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity]["participants"]
        
        # Then, unregister
        unregister_response = client.delete(
            f"/activities/{activity}/unregister?email={email}"
        )
        assert unregister_response.status_code == 200
        
        # Verify unregistration
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email not in activities[activity]["participants"]

    def test_multiple_signups_different_activities(self, client, reset_activities):
        """Test that a student can sign up for multiple different activities."""
        email = "multisport@mergington.edu"
        
        # Sign up for Chess Club
        response1 = client.post(f"/activities/Chess Club/signup?email={email}")
        assert response1.status_code == 200
        
        # Sign up for Art Club
        response2 = client.post(f"/activities/Art Club/signup?email={email}")
        assert response2.status_code == 200
        
        # Verify both signups
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities["Chess Club"]["participants"]
        assert email in activities["Art Club"]["participants"]

    def test_url_encoding_in_activity_names(self, client, reset_activities):
        """Test that activity names with spaces are properly URL encoded."""
        email = "urltest@mergington.edu"
        
        # Test with spaces in activity name
        response = client.post(
            "/activities/Programming%20Class/signup?email=" + email
        )
        assert response.status_code == 200
        
        # Verify signup
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities["Programming Class"]["participants"]

    def test_email_validation_in_params(self, client, reset_activities):
        """Test behavior with various email formats."""
        # Test with valid email
        response = client.post(
            "/activities/Chess Club/signup?email=valid.email@mergington.edu"
        )
        assert response.status_code == 200
        
        # Test with email containing special characters
        response = client.post(
            "/activities/Art Club/signup?email=test%2Bemail@mergington.edu"
        )
        assert response.status_code == 200