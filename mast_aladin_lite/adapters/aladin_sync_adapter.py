import astropy.units as u
from astropy.coordinates import SkyCoord
import numpy as np

from .viewer_sync_adapter import ViewerSyncAdapter
from mast_aladin_lite.app import gca


class AladinSyncAdapter(ViewerSyncAdapter):
    def __init__(self):
        self.viewer = gca()

    def get_center(self):
        return self.viewer.target

    def get_limits(self, wcs):
        """
        Aladin Lite defines its center as the screen's center in WCS. In contrast,
        Imviz uses the center pixel to infer the corners. This function calculates
        the sky coordinates of the four corners of the Aladin view using spherical
        offsets, then converts them to pixel coordinates using the Imviz WCS.

        Returns:
            tuple: (x_min, x_max, y_min, y_max) pixel coordinates in Imviz WCS.
        """
        if self.viewer._fov_xy == {}:
            raise ValueError("_fov_xy is not set due to a known issue in ipyaladin.")

        if self.viewer.target is None:
            raise ValueError("Target (SkyCoord) is not defined.")

        half_fov_x = self.viewer._fov_xy["x"] * u.deg / 2
        half_fov_y = self.viewer._fov_xy["y"] * u.deg / 2

        offsets = [
            (half_fov_x, half_fov_y),
            (-half_fov_x, half_fov_y),
            (half_fov_x, -half_fov_y),
            (-half_fov_x, -half_fov_y),
        ]

        corner_coords = [self.viewer.target.spherical_offsets_by(dx, dy) for dx, dy in offsets]
        x, y = wcs.world_to_pixel(SkyCoord(corner_coords))

        x_min, x_max = np.min(x), np.max(x)
        y_min, y_max = np.min(y), np.max(y)

        return x_min, x_max, y_min, y_max

    def get_fov(self):
        return {
            "x": self.viewer._fov_xy["x"] * u.deg,
            "y": self.viewer._fov_xy["y"] * u.deg
        }

    def sync_to(self, sync_viewer):
        self.viewer.target = sync_viewer.get_center()
        self.viewer.fov = sync_viewer.get_fov()["x"].to_value()

    def show(self):
        display(self.viewer)  # noqa:F821
