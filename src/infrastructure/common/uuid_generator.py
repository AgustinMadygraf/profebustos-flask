"""
Path: src/infrastructure/common/uuid_generator.py
"""

import uuid

from src.application.ports.id_generator import IdGenerator


class UUIDGenerator(IdGenerator):
    "UUIDv4 generator implementation."
    def new_id(self) -> str:
        return str(uuid.uuid4())
