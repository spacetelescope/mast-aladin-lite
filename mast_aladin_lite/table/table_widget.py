from traitlets import List, Unicode, Bool, Int, Any, observe
from ipypopout import PopoutButton
from ipyvuetify import VuetifyTemplate
from ipywidgets.widgets import widget_serialization

from mast_aladin_lite.table.mast import detect_mission, get_column_descriptions


def serialize(table):
    """
    Convert an astropy table to a list of dictionaries
    containing each column as a list of pure Python objects.
    """
    return [
        {
            k: v.tolist()
            for k, v in dict(row).items()
        } for row in table
    ]


class TableWidget(VuetifyTemplate):
    template_file = __file__, "table.vue"

    items = List().tag(sync=True)
    headers_visible = List().tag(sync=True)
    headers_avail = List().tag(sync=True)
    show_if_empty = Bool(True).tag(sync=True)
    show_rowselect = Bool(True).tag(sync=True)
    selected_rows = List().tag(sync=True)
    column_descriptions = List().tag(sync=True)
    multiselect = Bool(True).tag(sync=True)
    item_key = Unicode().tag(sync=True)
    clear_btn_lbl = Unicode('Clear Table').tag(sync=True)
    items_per_page = Int(5).tag(sync=True)
    popout_button = Any().tag(sync=True, **widget_serialization)
    show_tooltips = Bool(True).tag(sync=True)

    table = None
    row_select_callbacks = []

    def __init__(self, table, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.popout_button = PopoutButton(self)

        self.table = table

        self.items = serialize(table)
        mission = detect_mission(table)
        columns = table.colnames
        self.column_descriptions = get_column_descriptions(mission)

        default_keys = [
            'fileSetName',  # data products from Missions Mast
            'source_id',    # Gaia
            'MatchID',      # Hubble Source Catalog
            'objID',        # PanSTARRS
        ]
        for default_key in default_keys:
            if default_key in columns:
                self.item_key = default_key
                break

        self.headers_avail = columns

        # by default, remove the `s_region`` column
        # from the visible columns in the widget:
        if 's_region' in columns:
            columns.remove('s_region')

        self.headers_visible = columns

    @observe('selected_rows')
    def _on_row_selection(self, msg={}):
        for func in self.row_select_callbacks:
            func(msg)
