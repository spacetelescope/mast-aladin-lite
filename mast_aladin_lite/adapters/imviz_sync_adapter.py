from .viewer_sync_adapter import ViewerSyncAdapter


class ImvizSyncAdapter(ViewerSyncAdapter):
    def __init__(self, viewer=None):
        # todo: assert the type of the viewer is jdaviz/imviz
        from jdaviz.configs.imviz.helper import _current_app
        self.app = viewer if viewer else _current_app
        self.viewer = self.app.default_viewer

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

    def add_callback(self, func):
        self.viewer._obj.state.add_callback('x_min', func)

    def remove_callback(self, func):
        self.viewer._obj.state.remove_callback('x_min', func)

    def show(self):
        self.app.show()
        self.app.link_data(align_by='wcs')
        self.app.plugins['Orientation'].set_north_up_east_left()

    @property
    def _wcs(self):
        return self.viewer._obj.state.reference_data.coords
