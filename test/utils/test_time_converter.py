import pytest 
from utils.time_converter import parse_duration


def test_parse_duration_full_normal():
    duration_span = "1 hour 30 minutes"
    duration = parse_duration(duration_span)

    assert duration ==  90