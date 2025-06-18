import pytest
from mast_aladin_lite import MastAladin


@pytest.fixture
def MastAladin_app():
    return MastAladin()
