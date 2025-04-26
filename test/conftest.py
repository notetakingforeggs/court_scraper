import pytest
from pathlib import Path

@pytest.fixture
def daily_cause_list_aldershot_test() -> str :
    path = Path(__file__).parent/"resources"/"daily_cause_list_aldershot_test.html"
    return path.read_text(encoding="utf-8")