import os
import json
from collections import defaultdict

table_data_dir = os.path.join(os.path.dirname(__file__), 'data')
unique_column_path = os.path.join(table_data_dir, 'unique_columns_per_mission.json')
column_descriptions_path = os.path.join(table_data_dir, 'column_descriptions.json')

missions = ['jwst', 'roman', 'hst']


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
