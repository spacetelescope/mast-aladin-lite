import pytest
from mast_aladin_lite import MastAladin
from astropy.coordinates import SkyCoord


@pytest.fixture
def MastAladin_helper():
    return MastAladin()


def test_mast_aladin_has_aid(MastAladin_helper):
    assert hasattr(MastAladin_helper, 'aid')
    assert callable(getattr(MastAladin_helper.aid, 'set_viewport', None))


def test_mast_aladin_aid_set_viewport(MastAladin_helper):
    assert MastAladin_helper.target == SkyCoord(0, 0, unit='deg')
    target_coords = SkyCoord(45, 45, unit='deg')
    MastAladin_helper.aid.set_viewport(center=target_coords)
    assert MastAladin_helper.target == target_coords
