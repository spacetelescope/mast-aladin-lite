from astropy.coordinates import SkyCoord, Angle
import astropy.units as u
from astropy.tests.helper import assert_quantity_allclose
import numpy as np


def assert_coordinate_close(coord1, coord2, atol=1 * u.arcsec):
    # check that two coordinates are within some separation tolerance
    separation = coord1.separation(coord2)
    assert_quantity_allclose(separation, desired=0*u.arcsec, atol=atol)


def assert_angle_close(angle1, angle2, atol=1 * u.arcsec):
    # check that two angles are within some separation tolerance
    difference = np.abs(angle1 - angle2)
    assert_quantity_allclose(difference, desired=0*u.arcsec, atol=atol)


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


def test_mast_aladin_aid_get_viewport(MastAladin_helper):
    # check that the default center coordinate is (0, 0) deg and
    # the default fov is 60.0 deg
    default_center = SkyCoord(0, 0, unit='deg')
    default_viewport = MastAladin_helper.aid.get_viewport()
    assert_coordinate_close(default_viewport["center"], default_center)
    assert_angle_close(Angle(60, u.deg), default_viewport["fov"])


def test_mast_aladin_aid_get_and_set_viewport_roundtrip(MastAladin_helper):
    # check that performing a round trip of getting and setting the
    # viewport results in the original state

    # get default settings
    default_viewport = MastAladin_helper.aid.get_viewport()

    # change viewport settings
    target_coords = SkyCoord(45, 45, unit='deg')
    MastAladin_helper.aid.set_viewport(center=target_coords)

    # check new viewport settings
    midpoint_viewport = MastAladin_helper.aid.get_viewport()
    assert_coordinate_close(midpoint_viewport["center"], target_coords)
    assert_angle_close(Angle(60, u.deg), midpoint_viewport["fov"])

    # change viewport settings back to default
    MastAladin_helper.aid.set_viewport(center=default_viewport["center"])

    # check final viewport settings
    final_viewport = MastAladin_helper.aid.get_viewport()
    assert_coordinate_close(final_viewport["center"], default_viewport["center"])
    assert_angle_close(default_viewport["fov"], final_viewport["fov"])
