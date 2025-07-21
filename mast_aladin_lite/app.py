from ipyaladin import Aladin
from mast_aladin_lite.aida import AID
from mast_aladin_lite.table import MastTable


# store reference to the latest instantiation:
_latest_instantiated_app = None


class MastAladin(Aladin):

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


def gca():
    """
    Get the current mast-aladin-lite application instance.

    Returns
    -------
    MastAladin
    """
    return _latest_instantiated_app
