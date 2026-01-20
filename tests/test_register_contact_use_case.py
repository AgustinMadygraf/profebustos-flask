from use_cases.register_contact import RegisterContactUseCase


class FakeContactRepository:
    def __init__(self):
        self.saved = []

    def save(self, contact):
        self.saved.append(contact)
        return contact


class FakeIdGenerator:
    def __init__(self, value):
        self.value = value
        self.calls = 0

    def new_id(self):
        self.calls += 1
        return self.value


def test_register_contact_creates_ticket_and_saves_once():
    repo = FakeContactRepository()
    id_generator = FakeIdGenerator("fixed-id-123")
    use_case = RegisterContactUseCase(repo, id_generator)

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
    assert repo.saved[0] is not result
    assert result.ticket_id == "fixed-id-123"
    assert id_generator.calls == 1
