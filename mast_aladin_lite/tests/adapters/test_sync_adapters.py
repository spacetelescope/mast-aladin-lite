from astropy.coordinates import SkyCoord
from mast_aladin_lite.adapters import AladinSyncAdapter, ImvizSyncAdapter
from mast_aladin_lite.app import MastAladin
from mast_aladin_lite.tests.test_utils import BaseImviz

from pytest import approx


class TestSyncAdapters(BaseImviz):
    def test_aladin_sync_from_imviz(self):
        # arrange
        target = SkyCoord(9.4213055, -33.71625419, unit="deg")
        MastAladin(target=target, height=500)
        mast_aladin_sync_adapter = AladinSyncAdapter()

        imviz_sync_adapter = ImvizSyncAdapter()

        # assert starting coordinate is approximately on Cartwheel Galaxy
        center = mast_aladin_sync_adapter.get_center()
        assert center.ra.deg == approx(9.4213055, rel=1e-6)
        assert center.dec.deg == approx(-33.71625419, rel=1e-7)

        # act - sync the mast aladin viewer to the imviz view
        mast_aladin_sync_adapter.sync_to(imviz_sync_adapter)

        # assert that the view has changed as expected
        center = mast_aladin_sync_adapter.get_center()
        assert center.ra.deg == approx(9.425937637864708, rel=1e-14)
        assert center.dec.deg == approx(-33.71515927986813, rel=1e-14)

    def test_aladin_sync_to_imviz(self):
        # arrange
        target = SkyCoord(9.4213055, -33.71625419, unit="deg")
        MastAladin(target=target, height=500)
        mast_aladin_sync_adapter = AladinSyncAdapter()
        mast_aladin_sync_adapter.viewer._fov_xy = {'x': 60, 'y': 12.583892617449665}

        imviz_sync_adapter = ImvizSyncAdapter()

        # assert starting coordinate is approximately on Cartwheel Galaxy
        center = imviz_sync_adapter.get_center()
        assert center.ra.deg == approx(9.425937637864708, rel=1e-14)
        assert center.dec.deg == approx(-33.71515927986813, rel=1e-14)

        # act - sync the imviz viewer to the mast aladin viewer
        imviz_sync_adapter.sync_to(mast_aladin_sync_adapter)

        # assert that the view has changed as expected
        center = imviz_sync_adapter.get_center()
        assert center.ra.deg == approx(9.420758834360687, rel=1e-14)
        assert center.dec.deg == approx(-33.71643929028706, rel=1e-14)
