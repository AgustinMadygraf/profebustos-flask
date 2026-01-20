from src.application.dtos.contact_dto import ContactDTO
from src.application.errors import ContactCreateFailed, DatabaseUnavailable
from src.interface_adapters.controllers.contact_controller import ContactController


class FakeRequest:
    def __init__(self, payload):
        self.is_json = True
        self._payload = payload
        self.remote_addr = "127.0.0.1"
        self.headers = {"User-Agent": "pytest", "Origin": "http://localhost:5173"}
        self.path = "/v1/contact/email"

    def get_json(self):
        return self._payload


class FakeUseCase:
    def __init__(self, result=None, error=None):
        self.result = result
        self.error = error

    def execute(self, **kwargs):
        if self.error:
            raise self.error
        return self.result


def test_contact_controller_success_returns_ticket_id():
    use_case = FakeUseCase(
        result=ContactDTO(
            ticket_id="t-1",
            name="Ada",
            email="ada@example.com",
            company="Analytical Engines",
            message="Hello",
            page_location="/",
            traffic_source="direct",
            ip="127.0.0.1",
            user_agent="pytest",
            created_at=None,
        )
    )
    controller = ContactController(use_case)
    request = FakeRequest({
        "name": "Ada",
        "email": "ada@example.com",
        "company": "",
        "message": "",
        "page_location": "",
        "traffic_source": "",
    })

    response, status = controller.registrar_contacto(request)

    assert status == 201
    assert response["success"] is True
    assert response["ticket_id"] == "t-1"


def test_contact_controller_maps_contact_create_failed():
    use_case = FakeUseCase(error=ContactCreateFailed())
    controller = ContactController(use_case)
    request = FakeRequest({
        "name": "Ada",
        "email": "ada@example.com",
        "company": "",
        "message": "",
        "page_location": "",
        "traffic_source": "",
    })

    response, status = controller.registrar_contacto(request)

    assert status == 500
    assert response["error_code"] == "CONTACT_CREATE_FAILED"


def test_contact_controller_maps_db_unavailable():
    use_case = FakeUseCase(error=DatabaseUnavailable())
    controller = ContactController(use_case)
    request = FakeRequest({
        "name": "Ada",
        "email": "ada@example.com",
        "company": "",
        "message": "",
        "page_location": "",
        "traffic_source": "",
    })

    response, status = controller.registrar_contacto(request)

    assert status == 503
    assert response["error_code"] == "DB_UNAVAILABLE"
