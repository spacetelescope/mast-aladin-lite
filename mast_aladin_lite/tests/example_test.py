import pytest
from app import MastAladin


@pytest.fixture
def MastAladin_helper():
    return MastAladin()


def test_calling_app(MastAladin_helper):
    assert MastAladin_helper is MastAladin()
