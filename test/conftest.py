import pytest
from pathlib import Path

@pytest.fixture
def daily_cause_list_no_minors() -> str :
    path = Path(__file__).parent/"resources"/"daily_cause_list_no_minors.html"
    return path.read_text(encoding="utf-8")

@pytest.fixture
def daily_cause_list_mixed() -> str :
    path = Path(__file__).parent/"resources"/"daily_cause_list_mixed.html"
    return path.read_text(encoding="utf-8")