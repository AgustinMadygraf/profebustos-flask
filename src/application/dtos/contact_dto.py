"""
Path: src/application/dtos/contact_dto.py
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ContactDTO:
    ticket_id: str
    name: str
    email: str
    company: str
    message: str
    page_location: str
    traffic_source: str
    ip: str
    user_agent: str
    created_at: object = None
