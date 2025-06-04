from ipyaladin import Aladin
from astropy.coordinates import Angle
from jdaviz.utils import get_top_layer_index
from jdaviz.core.user_api import ViewerUserApi
import astropy.units as u
from astropy.coordinates import SkyCoord
import numpy as np

class MastAladin(Aladin):
    def set_orientation(self, viewer):
        if isinstance(viewer, ViewerUserApi):
            self.target, self.fov = self.get_imviz_orientation(viewer)
        else:
            print("Unsupported viewer type")

    def get_imviz_orientation(self, imviz_viewer):
        viewer = imviz_viewer._obj
        sky_cen = viewer._get_center_skycoord()
        imviz_fov = self._get_imviz_fov(viewer)

        return sky_cen, imviz_fov

    def set_imviz_orientation(self, imviz_viewer):
        viewer = imviz_viewer._obj
        viewer.set_limits(*self._get_aladin_limits(viewer))

    def _get_imviz_fov(self, imviz_viewer):
        """
        Aladin lite defines the FOV as the width of the viewer in 
        world coordinates. To calculate that for imviz, we need to 
        get the world coordinates of the lower left and right pixels 
        of the imviz viewer, and then calculate the separation between
        those points.
        """
        x_min = imviz_viewer.state.x_min
        x_max = imviz_viewer.state.x_max
        y_min = imviz_viewer.state.y_min

        wcs = imviz_viewer.state.reference_data.coords
        lower_left = wcs.pixel_to_world(x_min, y_min)
        lower_right = wcs.pixel_to_world(x_max, y_min)

        return lower_left.separation(lower_right)

    def _get_aladin_limits(self, imviz_viewer):
        """
        Calculate the pixel coordinate limits in the Imviz viewer corresponding 
        to the Aladin Lite field of view.

        Aladin Lite defines its center as the screen's center in WCS. In contrast, 
        Imviz uses the center pixel to infer the corners. This function calculates 
        the sky coordinates of the four corners of the Aladin view using spherical 
        offsets, then converts them to pixel coordinates using the Imviz WCS.

        Returns:
            tuple: (x_min, x_max, y_min, y_max) pixel coordinates in Imviz WCS.
        """
        if self._fov_xy == {}:
            raise ValueError("_fov_xy is not set due to a known issue in ipyaladin.")

        if self.target is None:
            raise ValueError("Target (SkyCoord) is not defined.")

        wcs = imviz_viewer.state.reference_data.coords
        half_fov_x = self._fov_xy["x"] * u.deg / 2
        half_fov_y = self._fov_xy["y"] * u.deg / 2

        offsets = [
            (half_fov_x,  half_fov_y),
            (-half_fov_x, half_fov_y),
            (half_fov_x, -half_fov_y),
            (-half_fov_x, -half_fov_y),
        ]

        corner_coords = [self.target.spherical_offsets_by(dx, dy) for dx, dy in offsets]
        x, y = wcs.world_to_pixel(SkyCoord(corner_coords))

        x_min, x_max = np.min(x), np.max(x)
        y_min, y_max = np.min(y), np.max(y)

        return x_min, x_max, y_min, y_max