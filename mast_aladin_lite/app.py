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

    @observe('clicked_object', 'clicked_footprint')
    def _on_object_clicked(self, data):
        self.info.value = f"<h3>Info</h3><p>{data}</p>"

        # if this is a catalog object selection:
        if 'ra' in data['new']:
            clicked_coord = [data['new']['ra'], data['new']['dec']]
            for item in self.selected_table.items:
                row_coord = [item['ra'], item['dec']]

                # only select row for exact RA+Dec matches:
                if all(np.isclose(row_coord, clicked_coord)):
                    self.selected_table.selected_rows = [item]
                    break

        else:
            # if the new selection isn't an object in the last-loaded catalog,
            # deselect the selected rows:
            self.selected_table.selected_rows = []

        return data
