import pytest
from services.data_validation import file_validation

def test_validate_file_format():
    assert file_validation.validate_file_format("data.csv") == True
    assert file_validation.validate_file_format("image.png") == False  # Invalid file format
