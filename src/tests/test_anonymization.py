import pytest
from src.services.anonymization import anonymize_email, anonymize_name

def test_anonymize_email():
    assert anonymize_email("test@example.com") == "****@example.com"
    assert anonymize_email("user123@gmail.com") == "****@gmail.com"

def test_anonymize_name():
    assert anonymize_name("John Doe") == "J*** D**"
    assert anonymize_name("Alice Johnson") == "A**** J******"
