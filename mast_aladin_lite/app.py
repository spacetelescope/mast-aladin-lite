from ipyaladin import Aladin
from mast_aladin_lite.aida import AID
from mast_aladin_lite.table import MastTable

from ipywidgets import widgets


# store reference to the latest instantiation:
_latest_instantiated_app = None


class MastAladin(Aladin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # the `aid` attribute gives access to methods from the
        # Astro Image Display (AID) API
        self.aid = AID(self)

        #
        self.selected_table = widgets.Output()

        global _latest_instantiated_app
        _latest_instantiated_app = self

    def load_table(self, table, name='table'):
        self.add_table(table, name=name, color="lime", shape="circle", source_size=10)
        table_widget = MastTable(table)
        self.tables[name] = self.selected_table = table_widget


def gca():
    """
    Get the current mast-aladin-lite application instance.

    Returns
    -------
    MastAladin
    """
    return _latest_instantiated_app
