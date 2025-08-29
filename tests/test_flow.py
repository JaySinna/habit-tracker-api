from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def get_token():
    # Register
    client.post("/auth/register", json={"email": "test@example.com", "password": "pw"})
    # Login
    r = client.post("/auth/login", json={"email": "test@example.com", "password": "pw"})
    return r.json()["access_token"]


def test_full_flow():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Create a habit
    h = client.post("/habits", json={"name": "Test Habit", "period": "daily"}, headers=headers)
    assert h.status_code == 201
    habit = h.json()
    habit_id = habit["id"]

    # Add a checkin
    c = client.post(f"/habits/{habit_id}/checkins", json={"day": "2025-08-27"}, headers=headers)
    assert c.status_code == 201

    # Fetch stats
    s = client.get("/habits/stats", headers=headers)
    assert s.status_code == 200
    stats = s.json()
    assert stats[0]["name"] == "Test Habit"
    assert stats[0]["current_streak"] >= 1
