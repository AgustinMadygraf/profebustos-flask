from interface_adapters.controllers.contact_controller import (
    sanitize_and_validate_contact_payload,
)


def test_sanitize_and_validate_returns_normalized_payload():
    data = {
        "name": "  Ada   Lovelace ",
        "email": "ada@example.com",
        "company": "  Analytical   Engines ",
        "message": "<b>Hello</b>  world",
        "page_location": " /pricing ",
        "traffic_source": " ads ",
    }

    error_response, error_status, normalized = sanitize_and_validate_contact_payload(data)

    assert error_response is None
    assert error_status is None
    assert normalized["name"] == "Ada Lovelace"
    assert normalized["company"] == "Analytical Engines"
    assert normalized["message"] == "Hello  world"
    assert normalized["page_location"] == "/pricing"
    assert normalized["traffic_source"] == "ads"


def test_sanitize_and_validate_rejects_invalid_email():
    data = {
        "name": "Ada",
        "email": "not-an-email",
        "company": "",
        "message": "",
        "page_location": "",
        "traffic_source": "",
    }

    error_response, error_status, normalized = sanitize_and_validate_contact_payload(data)

    assert normalized is None
    assert error_status == 400
    assert error_response["error"] == "El correo electrÃ³nico tiene un formato invÃ¡lido"
    assert "error_code" not in error_response
