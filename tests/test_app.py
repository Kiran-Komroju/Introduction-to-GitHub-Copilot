"""
Tests for the Mergington High School Activities API
"""
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    """Test that root endpoint redirects to static/index.html"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"

def test_get_activities():
    """Test getting all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0
    # Test structure of an activity
    activity = next(iter(data.values()))
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity

def test_signup_for_activity():
    """Test signing up for an activity"""
    # Get first activity name
    response = client.get("/activities")
    activities = response.json()
    activity_name = next(iter(activities.keys()))
    
    # Test successful signup
    email = "newstudent@mergington.edu"
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]

    # Verify student was added
    response = client.get("/activities")
    activities = response.json()
    assert email in activities[activity_name]["participants"]

def test_signup_validation():
    """Test signup validation cases"""
    # Test non-existent activity
    response = client.post("/activities/NonExistentClub/signup?email=test@mergington.edu")
    assert response.status_code == 404
    
    # Get first activity for duplicate signup test
    response = client.get("/activities")
    activities = response.json()
    activity_name = next(iter(activities.keys()))
    email = activities[activity_name]["participants"][0]
    
    # Test duplicate signup
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_unregister_from_activity():
    """Test unregistering from an activity"""
    # Get first activity with participants
    response = client.get("/activities")
    activities = response.json()
    activity_name = next(name for name, details in activities.items() 
                        if details["participants"])
    email = activities[activity_name]["participants"][0]
    
    # Test successful unregistration
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]

    # Verify student was removed
    response = client.get("/activities")
    activities = response.json()
    assert email not in activities[activity_name]["participants"]

def test_unregister_validation():
    """Test unregister validation cases"""
    # Test non-existent activity
    response = client.post("/activities/NonExistentClub/unregister?email=test@mergington.edu")
    assert response.status_code == 404
    
    # Get first activity
    response = client.get("/activities")
    activities = response.json()
    activity_name = next(iter(activities.keys()))
    
    # Test unregistering non-registered student
    response = client.post(f"/activities/{activity_name}/unregister?email=notregistered@mergington.edu")
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]