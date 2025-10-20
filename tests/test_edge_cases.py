"""
Edge case and integration tests for the FastAPI activities API.
"""

import pytest
from fastapi.testclient import TestClient


class TestEdgeCases:
    """Test class for edge cases and integration scenarios."""

    def test_activity_name_with_special_characters(self, client, reset_activities):
        """Test handling of activity names with special characters."""
        # Test activity names with spaces, which exist in our data
        response = client.post(
            "/activities/Chess Club/signup?email=special@mergington.edu"
        )
        assert response.status_code == 200

    def test_email_with_plus_sign(self, client, reset_activities):
        """Test email addresses with plus signs (common email feature)."""
        import urllib.parse
        
        email = "student+test@mergington.edu"
        # Properly URL encode the email
        encoded_email = urllib.parse.quote(email)
        
        response = client.post(
            f"/activities/Chess Club/signup?email={encoded_email}"
        )
        assert response.status_code == 200
        
        # Verify the participant was added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities["Chess Club"]["participants"]

    def test_case_sensitivity_in_activity_names(self, client, reset_activities):
        """Test that activity names are case sensitive."""
        # This should fail because "chess club" != "Chess Club"
        response = client.post(
            "/activities/chess club/signup?email=case@mergington.edu"
        )
        assert response.status_code == 404

    def test_empty_email_parameter(self, client, reset_activities):
        """Test behavior with empty email parameter."""
        response = client.post("/activities/Chess Club/signup?email=")
        # The API should still process this (empty string is valid for our current implementation)
        assert response.status_code == 200

    def test_missing_email_parameter(self, client, reset_activities):
        """Test behavior when email parameter is missing."""
        response = client.post("/activities/Chess Club/signup")
        assert response.status_code == 422  # Unprocessable Entity (missing required parameter)

    def test_activity_participants_persistence(self, client, reset_activities):
        """Test that participant changes persist across multiple requests."""
        email1 = "persist1@mergington.edu"
        email2 = "persist2@mergington.edu"
        activity = "Art Club"
        
        # Add first participant
        response1 = client.post(f"/activities/{activity}/signup?email={email1}")
        assert response1.status_code == 200
        
        # Add second participant
        response2 = client.post(f"/activities/{activity}/signup?email={email2}")
        assert response2.status_code == 200
        
        # Check that both participants are present
        activities_response = client.get("/activities")
        activities = activities_response.json()
        participants = activities[activity]["participants"]
        assert email1 in participants
        assert email2 in participants
        
        # Remove first participant
        unregister_response = client.delete(f"/activities/{activity}/unregister?email={email1}")
        assert unregister_response.status_code == 200
        
        # Check that only second participant remains
        activities_response = client.get("/activities")
        activities = activities_response.json()
        participants = activities[activity]["participants"]
        assert email1 not in participants
        assert email2 in participants

    def test_all_activities_have_required_fields(self, client, reset_activities):
        """Test that all activities have the required fields."""
        response = client.get("/activities")
        assert response.status_code == 200
        
        activities = response.json()
        required_fields = ["description", "schedule", "max_participants", "participants"]
        
        for activity_name, activity_data in activities.items():
            for field in required_fields:
                assert field in activity_data, f"Missing field '{field}' in activity '{activity_name}'"
            
            # Check data types
            assert isinstance(activity_data["description"], str)
            assert isinstance(activity_data["schedule"], str)
            assert isinstance(activity_data["max_participants"], int)
            assert isinstance(activity_data["participants"], list)
            assert activity_data["max_participants"] > 0

    def test_participants_list_contains_only_strings(self, client, reset_activities):
        """Test that participants lists contain only string email addresses."""
        response = client.get("/activities")
        assert response.status_code == 200
        
        activities = response.json()
        for activity_name, activity_data in activities.items():
            participants = activity_data["participants"]
            for participant in participants:
                assert isinstance(participant, str), f"Non-string participant in {activity_name}: {participant}"
                assert "@" in participant, f"Invalid email format in {activity_name}: {participant}"