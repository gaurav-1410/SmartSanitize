import pytest
from src.services.data_validation import validate_file_format

def test_validate_file_format():
    assert validate_file_format("data.csv") == True
    assert validate_file_format("image.png") == False  # Invalid file format
