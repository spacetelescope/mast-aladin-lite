from .viewer_sync_adapter import ViewerSyncAdapter


class ImvizSyncAdapter(ViewerSyncAdapter):
    def __init__(self, viewer):
        # todo: assert the type of the viewer is jdaviz/imviz
        self.viewer = viewer

    def get_center(self):
        return self.viewer._obj._get_center_skycoord()

    def get_limits(self, wcs):
        x_min, x_max = self.viewer._obj.state.x_min, self.viewer._obj.state.x_max
        y_min, y_max = self.viewer._obj.state.y_min, self.viewer._obj.state.y_max

        # todo: convert from the imviz wcs into the wcs passed to get_limits
        return x_min, x_max, y_min, y_max

    def get_fov(self):
        x_min, x_max = self.viewer._obj.state.x_min, self.viewer._obj.state.x_max
        y_min, y_max = self.viewer._obj.state.y_min, self.viewer._obj.state.y_max

        lower_left = self._wcs.pixel_to_world(x_min, y_min)
        lower_right = self._wcs.pixel_to_world(x_max, y_min)
        upper_left = self._wcs.pixel_to_world(x_min, y_max)

        return {
            "x": lower_left.separation(lower_right),
            "y": lower_left.separation(upper_left)
        }

    def sync_to(self, sync_viewer):
        self.viewer._obj.set_limits(*sync_viewer.get_limits(self._wcs))

    @property
    def _wcs(self):
        return self.viewer._obj.state.reference_data.coords
