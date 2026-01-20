from datetime import datetime

from src.entities.contact import Contact
from src.infrastructure.flask import flask_app


def test_get_contact_list_returns_expected_shape(monkeypatch):
    sample_contacts = [
        Contact(
            ticket_id="t-1",
            name="Ada Lovelace",
            email="ada@example.com",
            company="Analytical Engines",
            message="Hello",
            page_location="/",
            traffic_source="direct",
            ip="127.0.0.1",
            user_agent="pytest",
            created_at=datetime(2024, 1, 1, 12, 0, 0),
        )
    ]

    def fake_execute():
        return sample_contacts

    monkeypatch.setattr(
        flask_app,
        "list_contacts_use_case",
        type("UC", (), {"execute": staticmethod(fake_execute)}),
    )
    monkeypatch.setenv("FLASK_ENV", "development")

    client = flask_app.app.test_client()
    response = client.get("/v1/contact/list", headers={"Origin": "http://localhost:5173"})

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["success"] is True
    assert isinstance(payload["contactos"], list)
    assert payload["contactos"][0]["ticket_id"] == "t-1"
    assert payload["contactos"][0]["created_at"] is not None
