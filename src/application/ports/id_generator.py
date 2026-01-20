"""
Path: src/application/ports/id_generator.py
"""

from typing import Protocol


class IdGenerator(Protocol):
    "Generates new identifiers for application use cases."
    def new_id(self) -> str:
        "Return a new unique identifier."
        raise NotImplementedError
