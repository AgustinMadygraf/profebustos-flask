import re

from use_cases.register_contact import RegisterContactUseCase


class FakeContactRepository:
    def __init__(self):
        self.saved = []

    def save(self, contact):
        self.saved.append(contact)
        return contact


def test_register_contact_creates_ticket_and_saves_once():
    repo = FakeContactRepository()
    use_case = RegisterContactUseCase(repo)

    result = use_case.execute(
        name="Ada Lovelace",
        email="ada@example.com",
        company="Analytical Engines",
        message="Hello",
        page_location="/",
        traffic_source="direct",
        ip="127.0.0.1",
        user_agent="pytest",
    )

    assert len(repo.saved) == 1
    assert repo.saved[0] is result
    assert re.match(r"^[0-9a-f-]{36}$", result.ticket_id)
