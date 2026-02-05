import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_for_activity_success():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Remove if already present
    client.delete(f"/activities/{activity}/unregister?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Clean up
    client.delete(f"/activities/{activity}/unregister?email={email}")

def test_signup_for_activity_duplicate():
    email = "testuser2@mergington.edu"
    activity = "Chess Club"
    # Ensure user is signed up
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    # Clean up
    client.delete(f"/activities/{activity}/unregister?email={email}")

def test_signup_for_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

# ===== EDGE CASES TESTS =====

def test_signup_with_invalid_domain():
    """Test that only @mergington.edu emails are accepted"""
    invalid_emails = [
        "student@gmail.com",
        "teacher@yahoo.com",
        "someone@mergingtown.edu",  # Similar but wrong
        "admin@mergington.com",  # Wrong TLD
        "test@"
    ]
    activity = "Chess Club"
    for email in invalid_emails:
        response = client.post(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 400, f"Failed for email: {email}"
        assert "mergington.edu" in response.json()["detail"].lower()

def test_signup_with_empty_email():
    """Test signup with empty or whitespace-only email"""
    invalid_emails = ["", "   ", "\t", "\n"]
    activity = "Chess Club"
    for email in invalid_emails:
        response = client.post(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 400
        assert "invalid" in response.json()["detail"].lower() or "required" in response.json()["detail"].lower()

def test_signup_with_malformed_email():
    """Test signup with malformed emails"""
    malformed_emails = [
        "notanemail",
        "@mergington.edu",
        "student@@mergington.edu",
        "student @mergington.edu",  # Space in email
        "student@mergington .edu",
        "student@.edu"
    ]
    activity = "Chess Club"
    for email in malformed_emails:
        response = client.post(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 400, f"Failed for email: {email}"

def test_signup_for_full_activity():
    """Test that signup fails when activity is at max capacity"""
    # Create a small activity for testing
    activity = "Chess Club"
    max_capacity = activities[activity]["max_participants"]
    
    # Fill the activity to max capacity
    test_emails = [f"student{i}@mergington.edu" for i in range(max_capacity)]
    
    # First, clear existing participants
    activities[activity]["participants"] = []
    
    # Add students up to max capacity
    for email in test_emails:
        response = client.post(f"/activities/{activity}/signup?email={email}")
        if len(activities[activity]["participants"]) < max_capacity:
            assert response.status_code == 200
    
    # Try to add one more (should fail)
    overflow_email = "overflow@mergington.edu"
    response = client.post(f"/activities/{activity}/signup?email={overflow_email}")
    assert response.status_code == 400
    assert "full" in response.json()["detail"].lower() or "capacity" in response.json()["detail"].lower()
    
    # Clean up
    activities[activity]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]

def test_signup_with_sql_injection_attempt():
    """Test that SQL injection patterns are handled safely"""
    injection_patterns = [
        "'; DROP TABLE activities; --@mergington.edu",
        "admin'--@mergington.edu",
        "1' OR '1'='1@mergington.edu"
    ]
    activity = "Chess Club"
    for email in injection_patterns:
        response = client.post(f"/activities/{activity}/signup?email={email}")
        # Should either reject as invalid email or handle safely (not crash)
        assert response.status_code in [400, 422], f"Unexpected status for: {email}"

def test_signup_with_xss_attempt():
    """Test that XSS patterns in email are handled"""
    xss_patterns = [
        "<script>alert('xss')</script>@mergington.edu",
        "test<img src=x>@mergington.edu",
        "javascript:alert(1)@mergington.edu"
    ]
    activity = "Chess Club"
    for email in xss_patterns:
        response = client.post(f"/activities/{activity}/signup?email={email}")
        # Should reject as invalid email format
        assert response.status_code == 400, f"Failed to reject XSS attempt: {email}"

def test_signup_with_very_long_email():
    """Test signup with extremely long email"""
    long_email = "a" * 1000 + "@mergington.edu"
    response = client.post(f"/activities/Chess Club/signup?email={long_email}")
    assert response.status_code == 400
    assert "too long" in response.json()["detail"].lower() or "invalid" in response.json()["detail"].lower()

def test_signup_activity_name_case_sensitive():
    """Test that activity names are case-sensitive"""
    response = client.post("/activities/chess club/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_signup_with_special_characters_in_activity():
    """Test activity names with special characters"""
    special_names = [
        "Chess Club<script>",
        "../../../etc/passwd",
        "Chess%20Club",
        "Chess Club; DELETE"
    ]
    for activity_name in special_names:
        response = client.post(f"/activities/{activity_name}/signup?email=test@mergington.edu")
        # Should return 404 (not found) since these activities don't exist
        assert response.status_code == 404

def test_signup_with_unicode_characters():
    """Test emails with unicode characters"""
    unicode_emails = [
        "stüdent@mergington.edu",
        "学生@mergington.edu",
        "тест@mergington.edu"
    ]
    activity = "Chess Club"
    for email in unicode_emails:
        response = client.post(f"/activities/{activity}/signup?email={email}")
        # Should handle gracefully (either accept if valid or reject properly)
        assert response.status_code in [200, 400, 422]

def test_unregister_nonexistent_user():
    """Test unregistering a user that was never registered"""
    response = client.delete("/activities/Chess Club/unregister?email=nonexistent@mergington.edu")
    # Should return appropriate status (404 or 400)
    assert response.status_code in [400, 404, 200]  # Depends on implementation

def test_concurrent_signups_same_user():
    """Test potential race condition with same user signing up multiple times"""
    email = "racetest@mergington.edu"
    activity = "Chess Club"
    # Clean up first
    client.delete(f"/activities/{activity}/unregister?email={email}")
    
    # First signup should succeed
    response1 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response1.status_code == 200
    
    # Immediate second signup should fail
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400
    
    # Clean up
    client.delete(f"/activities/{activity}/unregister?email={email}")
