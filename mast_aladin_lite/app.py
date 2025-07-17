from astropy.coordinates import SkyCoord
import astropy.units as u
from astropy.utils.masked import Masked

from ipyaladin import Aladin
from mast_aladin_lite.aida import AID
from mast_aladin_lite.table import MastTable


# store reference to the latest instantiation:
_latest_instantiated_app = None


class MastAladin(Aladin):
    selected_table = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # the `aid` attribute gives access to methods from the
        # Astro Image Display (AID) API
        self.aid = AID(self)

        global _latest_instantiated_app
        _latest_instantiated_app = self

    def load_table(self, table, name='table', load_footprints=True, update_viewport=True):
        table_widget = MastTable(table)
        self.selected_table = table_widget

        if load_footprints:
            if 's_region' in table.colnames:
                self.add_graphic_overlay_from_stcs(table['s_region'])
            else:
                raise ValueError(
                    "The table does not contain an `s_region` column, so no "
                    "footprints can be loaded."
                )

        if update_viewport:
            ra_column, dec_column = 'ra', 'dec'

            if ra_column not in table.colnames:
                ra_column, dec_column = 'targ_ra', 'targ_dec'

            mask = (table[ra_column] == 0) & (table[dec_column] == 0)

            center_coord = SkyCoord(
                ra=Masked(table[ra_column] * u.deg, mask).mean().unmasked,
                dec=Masked(table[dec_column] * u.deg, mask).mean().unmasked,
                unit=u.deg
            )

            # change the coordinate frame to match the coordinates in the MAST table:
            self.coo_frame = 'ICRSd'
            self.target = center_coord

        return table_widget


def gca():
    """
    Get the current mast-aladin-lite application instance.

    Returns
    -------
    MastAladin
    """
    return _latest_instantiated_app
