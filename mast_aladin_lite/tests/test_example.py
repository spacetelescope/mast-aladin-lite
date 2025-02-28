import pytest
from mast_aladin_lite.app import MastAladin


@pytest.fixture
def MastAladin_helper():
    return MastAladin()


def test_instance_creation(MastAladin_helper):
    assert isinstance(MastAladin_helper, MastAladin)
