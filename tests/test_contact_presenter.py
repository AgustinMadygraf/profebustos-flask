from src.application.dtos.contact_dto import ContactDTO
from src.interface_adapters.presenters.contact_presenter import ContactPresenter


def test_contact_presenter_to_response():
    contact = ContactDTO(
        ticket_id="t-1",
        name="Ada",
        email="ada@example.com",
        company="Analytical Engines",
        message="Hello",
        page_location="/",
        traffic_source="direct",
        ip="127.0.0.1",
        user_agent="pytest",
        created_at="2024-01-01T12:00:00Z",
    )

    payload = ContactPresenter.to_response(contact)

    assert payload["ticket_id"] == "t-1"
    assert "created_at" not in payload


def test_contact_presenter_to_response_with_created_at():
    contact = ContactDTO(
        ticket_id="t-1",
        name="Ada",
        email="ada@example.com",
        company="Analytical Engines",
        message="Hello",
        page_location="/",
        traffic_source="direct",
        ip="127.0.0.1",
        user_agent="pytest",
        created_at="2024-01-01T12:00:00Z",
    )

    payload = ContactPresenter.to_response_with_created_at(contact)

    assert payload["ticket_id"] == "t-1"
    assert payload["created_at"] == "2024-01-01T12:00:00Z"
