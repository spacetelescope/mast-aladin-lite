from ipyaladin import Aladin
from mast_aladin_lite.aida import AID
from mast_aladin_lite.table import MastTable
from mast_aladin_lite.mixins import DelayUntilRendered


# store reference to the latest instantiation:
_latest_instantiated_app = None


class MastAladin(Aladin, DelayUntilRendered):

    def __init__(self, *args, **kwargs):
        # set ICRSd as the default visible coordinate system
        # in aladin-lite:
        kwargs.setdefault('coo_frame', 'ICRSd')

        super().__init__(*args, **kwargs)

        # the `aid` attribute gives access to methods from the
        # Astro Image Display (AID) API
        self.aid = AID(self)

        global _latest_instantiated_app
        _latest_instantiated_app = self

    def load_table(
        self,
        table,
        load_footprints=True,
        update_viewport=True,
        unique_column=None
    ):
        table_widget = MastTable(
            table,
            app=self,
            unique_column=unique_column,
            update_viewport=update_viewport
        )

        if load_footprints:
            if 's_region' in table.colnames:
                self.add_graphic_overlay_from_stcs(table['s_region'])
            else:
                raise ValueError(
                    "The table does not contain an `s_region` column, so no "
                    "footprints can be loaded."
                )

        return table_widget

    def vue_open_selected_rows_in_jdaviz(self, *args):
        from jdaviz.configs.imviz.helper import _current_app as viz

        with viz.batch_load():
            for filename in self.table_selected['filename']:
                if filename in [data.label for data in viz.app.data_collection]:
                    continue

                uri = f"mast:jwst/product/{filename}"
                viz.load_data(uri, cache=True)

        orientation = viz.plugins['Orientation']
        orientation.align_by = 'WCS'
        orientation.set_north_up_east_left()

        plot_options = viz.plugins['Plot Options']

        for layer in plot_options.layer.choices:
            plot_options.layer = layer
            plot_options.image_color_mode = 'One color per layer'
            plot_options.image_bias = 0.3
            plot_options.image_contrast = 1

        plot_options.apply_RGB_presets()

    def vue_open_selected_rows_in_aladin(self, *args):
        from mast_aladin_lite.app import _latest_instantiated_app

        for filename in self.table_selected['filename']:
            _latest_instantiated_app.add_fits(filename)


def gca():
    """
    Get the current mast-aladin-lite application instance.

    Returns
    -------
    MastAladin
    """
    return _latest_instantiated_app
