import pytest
from mast_aladin_lite import MastAladin
from astropy.coordinates import SkyCoord


@pytest.fixture
def MastAladin_helper():
    return MastAladin()

def test_mast_aladin_has_aid(MastAladin_helper):
    assert hasattr(MastAladin_helper, 'aid')
    assert callable(getattr(MastAladin_helper.aid, 'center_on', None))
