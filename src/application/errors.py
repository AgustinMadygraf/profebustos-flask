"""
Path: src/application/errors.py
"""


class ApplicationError(Exception):
    "Base class for application-level errors."


class ContactCreateFailed(ApplicationError):
    "Raised when a contact cannot be persisted."


class ContactListFailed(ApplicationError):
    "Raised when the contact list cannot be retrieved."


class DatabaseUnavailable(ApplicationError):
    "Raised when the database is unavailable."
