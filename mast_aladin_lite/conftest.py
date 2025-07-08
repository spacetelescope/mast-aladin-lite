import pytest
from mast_aladin_lite import MastAladin
from jdaviz import Imviz


@pytest.fixture
def MastAladin_app():
    return MastAladin()


@pytest.fixture
def imviz_helper():
    return Imviz()
