from astropy.coordinates import SkyCoord
from astropy.wcs import WCS

class ViewerSyncAdapter:
    def get_center(self) -> SkyCoord:
        raise NotImplementedError

    def get_limits(self, wcs) -> WCS:
        raise NotImplementedError

    def get_fov(self) -> dict:
        raise NotImplementedError

    def sync_to(self, sync_viewer):
        raise NotImplementedError