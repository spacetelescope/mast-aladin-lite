from astropy.coordinates import SkyCoord
from astropy.wcs import WCS
from abc import ABC, abstractmethod


class ViewerSyncAdapter(ABC):
    @abstractmethod
    def get_center(self) -> SkyCoord:
        raise NotImplementedError

    @abstractmethod
    def get_limits(self, wcs) -> WCS:
        raise NotImplementedError

    @abstractmethod
    def get_fov(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def sync_to(self, sync_viewer):
        raise NotImplementedError

    @abstractmethod
    def show(self):
        raise NotImplementedError
