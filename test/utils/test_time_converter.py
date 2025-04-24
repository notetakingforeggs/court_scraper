import pytest 
from utils.time_converter import parse_duration



@pytest.mark.parametrize("raw, expected", [
    ("1 hour 30 minutes", 90),
    (" 1r/ hour", 60),
    ("30r/ minutes", 30),
    ("30 minutes", 30),
    ("3 hours", 180),
    ("", None),
    (" ", None),
    ("30 munuds", 30),
    ("1 awr", 60)
])

def test_parse_duration(raw, expected):
    assert parse_duration(raw) == expected

