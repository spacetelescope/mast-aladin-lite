
import os
import json
from collections import defaultdict
from traitlets import List, Unicode, Bool, Int, Any, observe
from ipypopout import PopoutButton
from ipyvuetify import VuetifyTemplate
from ipywidgets.widgets import widget_serialization


# locations for metadata from MissionMAST:
missions = ['jwst', 'roman', 'hst']
table_data_dir = os.path.join(os.path.dirname(__file__), 'data')
unique_column_path = os.path.join(table_data_dir, 'unique_columns_per_mission.json')
column_descriptions_path = os.path.join(table_data_dir, 'column_descriptions.json')

# register loaded table widgets as they're initialized
_table_widgets = dict()


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


class MastTable(VuetifyTemplate):
    """
    Table widget for observation queries from Mission MAST.
    """
    template_file = __file__, "mast_table.vue"

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
    show_tooltips = Bool(False).tag(sync=True)
    menu_open = Bool(False).tag(sync=True)

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

        _table_widgets[len(_table_widgets)] = self

    @observe('selected_rows')
    def _on_row_selection(self, msg={}):
        for func in self.row_select_callbacks:
            func(msg)


def get_current_table():
    """
    Return the last instantiated table widget.
    """
    latest_table_index = list(_table_widgets.keys())[-1]
    return _table_widgets[latest_table_index]


def update_mast_column_lists(update_column_descriptions=True, update_unique_columns=True):
    """
    Return a dictionary of columns in observation query
    results from astroqery.mast.missions.MastMissions
    that are unique to each mission.
    """
    from astroquery.mast.missions import MastMissions

    mast = MastMissions()

    columns_available = dict()
    unique_columns = dict()
    column_descriptions = defaultdict(list)

    for mission in missions:
        mast.mission = mission
        column_list = mast.get_column_list()

        for row in column_list.iterrows():
            column_descriptions[mission].append(
                {k: str(v).strip() for k, v in zip(column_list.colnames, row)}
            )

        column_names = column_list['name'].tolist()
        columns_available[mission] = set(column_names)

    if update_column_descriptions:
        json_file = open(column_descriptions_path, 'w')
        json.dump(column_descriptions, json_file)

    for mission in missions:
        mast.mission = mission
        column_names = mast.get_column_list()['name']

        other_missions = list(missions)
        other_missions.remove(mission)
        other_mission_columns = columns_available[other_missions[0]].union(
            columns_available[other_missions[1]]
        )
        unique_columns[mission] = list(
            columns_available[mission].difference(
                other_mission_columns
            )
        )

    if update_unique_columns:
        json_file = open(unique_column_path, 'w')
        json.dump(unique_columns, json_file, indent=4)

    return unique_columns


def detect_mission(table):
    """
    Detect which mission was queried by the results from an astroquery.mast.missions
    query by looking for unique columns in the `astropy.table.Table`.
    """
    unique_columns = json.load(open(unique_column_path, 'r'))
    columns = table.colnames

    for mission in missions:
        if any(name in unique_columns[mission] for name in columns):
            return mission


def get_column_descriptions(mission):
    column_descriptions = json.load(open(column_descriptions_path, 'r'))
    return column_descriptions[mission]
