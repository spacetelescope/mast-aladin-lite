import numpy as np
from ipyvuetify import VuetifyTemplate
from traitlets import List, Unicode, Bool, Int, Any, observe
from ipypopout import PopoutButton
from ipywidgets.widgets import widget_serialization


def make_value_serializable(x):
    # empty values are `MaskedConstant`s, which
    # can't be serialized, so represent with `None`
    if isinstance(x, np.ma.core.MaskedConstant):
        return None
    elif isinstance(x, np.bool_):
        return bool(x)
    elif isinstance(x, np.floating):
        return float(x)
    elif isinstance(x, np.str_):
        return str(x)
    elif isinstance(x, np.integer):
        return int(x)
    return x

def serialize(table):
    return [
        {
            k: make_value_serializable(v)
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
    item_key = Unicode().tag(sync=True)
    clear_btn_lbl = Unicode('Clear Table').tag(sync=True)
    items_per_page = Int(5).tag(sync=True)
    popout_button = Any().tag(sync=True, **widget_serialization)
    
    table = None
    row_select_callbacks = []
    mast_aladin = None

    def __init__(self, table, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.popout_button = PopoutButton(self)

        self.table = table
        
        self.items = serialize(table)

        columns = list(self.items[0].keys())

        default_keys = [
            'fileSetName', # data products from Missions Mast
            'source_id', # Gaia
            'MatchID'  # Hubble Source Catalog
        ]
        for default_key in default_keys:
            if default_key in columns:
                self.item_key = default_key
                break

        self.headers_avail = columns

        # for now, pop out the s_region column
        # from the visible list
        if 's_region' in columns:
            columns.remove('s_region')
        self.headers_visible = columns

    @observe('selected_rows')
    def _on_row_selection(self, msg={}):
        for func in self.row_select_callbacks:
            func(msg)
