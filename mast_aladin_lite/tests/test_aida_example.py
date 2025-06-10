import pytest
from mast_aladin_lite import MastAladin
from astropy.coordinates import SkyCoord
import astropy.units as u
from astropy.tests.helper import assert_quantity_allclose


@pytest.fixture
def MastAladin_helper():
    return MastAladin()

def assert_coordinate_close(coord1, coord2, atol=1 * u.arcsec):
    # check that two coordinates are within some separation tolerance
    separation = coord1.separation(coord2)
    assert_quantity_allclose(separation, atol=atol)

def test_mast_aladin_has_aid(MastAladin_helper):
    assert hasattr(MastAladin_helper, 'aid')
    assert callable(getattr(MastAladin_helper.aid, 'set_viewport', None))


def test_mast_aladin_aid_set_viewport(MastAladin_helper):
    # check that the default center coordinate is (0, 0) deg before
    # we test the setter for center:
    default_center = SkyCoord(0, 0, unit='deg')
    assert_coordinate_close(MastAladin_helper.target, default_center)
    target_coords = SkyCoord(45, 45, unit='deg')
    MastAladin_helper.aid.set_viewport(center=target_coords)
    assert_coordinate_close(MastAladin_helper.target, target_coords)
