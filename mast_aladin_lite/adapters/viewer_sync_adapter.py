from abc import ABC, abstractmethod

from astropy.coordinates import SkyCoord
from astropy.wcs import WCS


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
    def add_callback(self, func):
        raise NotImplementedError

    @abstractmethod
    def remove_callback(self, func):
        raise NotImplementedError

    @abstractmethod
    def show(self):
        raise NotImplementedError
