import numpy as np
from ipyvuetify import VuetifyTemplate
from traitlets import List, Unicode, Bool, Int, observe


def serialize(table):
    return [
        {
            k: v 
            # empty values are `MaskedConstant`s, which
            # can't be serialized, so represet with `None`
            if v != np.ma.core.MaskedConstant else None
            for k, v in dict(row).items()
        } for row in table
    ]


class Table(VuetifyTemplate):
    template_file = __file__, "table.vue"
    
    items = List().tag(sync=True)
    headers_visible = List().tag(sync=True)
    headers_avail = List().tag(sync=True)
    show_if_empty = Bool(True).tag(sync=True)
    show_rowselect = Bool(True).tag(sync=True)
    selected_rows = List().tag(sync=True)
    multiselect = Bool(True).tag(sync=True)
    item_key = Unicode('fileSetName').tag(sync=True)
    clear_btn_lbl = Unicode('Clear Table').tag(sync=True)
    items_per_page = Int(3).tag(sync=True)

    table = None
    row_select_callbacks = []

    def __init__(self, table, *args, mast_aladin=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.table = table
        
        self.items = serialize(table)

        columns = list(self.items[0].keys())
        self.headers_avail = columns


        # for now, pop out the s_region column
        # from the visible list
        columns.remove('s_region')
        self.headers_visible = columns

    @observe('selected_rows')
    def _on_row_selection(self, msg={}):
        for func in self.row_select_callbacks:
            func(msg)
