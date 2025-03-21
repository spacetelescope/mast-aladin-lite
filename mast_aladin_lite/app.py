from ipyaladin import Aladin
from mast_aladin_lite.table import Table
import numpy as np
from traitlets import observe
from ipywidgets import widgets


class MastAladin(Aladin):
    tables = {}
    selected_table = None
    info = widgets.HTML()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.selected_table = widgets.Output()

    def load_table(self, table, name='table'):
        self.add_table(table, name=name, color="lime", shape="circle", source_size=10)
        table_widget = Table(table)
        self.tables[name] = self.selected_table = table_widget

    @observe('clicked_object')
    def _on_object_clicked(self, data):
        self.info.value = f"<h3>Info</h3><p>{data}</p>"

        # if this is a catalog object selection:
        if 'ra' in data['new']:
            ra = self.selected_table.table['ra']
            dec = self.selected_table.table['dec']
            dist = np.hypot(ra - data['new']['ra'], dec - data['new']['dec'])
            closest_idx = np.argmin(dist)
            self.selected_table.selected_rows = [self.selected_table.items[closest_idx]]
        else:
            # if the new selection isn't an object in the last-loaded catalog,
            # deselect the selected rows:
            self.selected_table.selected_rows = []

        return data
