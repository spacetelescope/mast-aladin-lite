import solara
import warnings
from collections import namedtuple
from ipyaladin import Aladin
from sidecar import Sidecar

from mast_aladin_lite.app import MastAladin, gca

__all__ = [
    'sidecar'
]


def sidecar(
    *apps,
    anchor='split-bottom',
    use_current_apps=False,
    title='mast-aladin-lite & jdaviz'
):
    jdaviz_instances = []

    try:
        from jdaviz.core.helpers import ConfigHelper
        from jdaviz.configs.imviz.helper import Imviz, _current_app as viz

        jdaviz_instances = [app for app in apps if isinstance(app, ConfigHelper)]

        # construct new imviz if not using current app or no current app exists:
        if not use_current_apps or (use_current_apps and viz is None):
            viz = Imviz()
            jdaviz_instances.append(viz)

    except ImportError:
        warnings.warn(
            "`sidecar` would open jdaviz, but it is not installed. To install it, "
            "run `pip install jdaviz`.",
            UserWarning
        )

    mal_instances = [app for app in apps if isinstance(app, Aladin)]

    if not len(mal_instances):
        mal = gca()
        if not use_current_apps or (use_current_apps and mal is None):
            mal = MastAladin()
        mal_instances.append(mal)

    @solara.component
    def Page(viz=viz, mal=mal):
        n_columns = sum(
            len(instances) for instances in [mal_instances, jdaviz_instances]
        )

        # create layout with `n_columns` equal width columns
        with solara.Columns(n_columns * [1], gutters_dense=True):

            for mal in mal_instances:
                with solara.Column():
                    mal.height = 600
                    solara.display(mal)

            for viz in jdaviz_instances:
                with solara.Column():
                    solara.display(viz.app)

    with Sidecar(anchor=anchor, title=title):
        solara.display(Page())

    apps_in_sidecar = namedtuple('Apps', ['mast_aladin_lite', 'jdaviz'])

    return apps_in_sidecar(
        mast_aladin_lite=mal_instances,
        jdaviz=jdaviz_instances,
    )
