import solara
import warnings
from sidecar import Sidecar

from mast_aladin_lite.app import MastAladin

__all__ = [
    'sidecar'
]


def sidecar(viz=None, mal=None, anchor='split-bottom', title='jdaviz & mast-aladin-lite'):
    if viz is None:
        try:
            from jdaviz.configs.imviz.helper import Imviz, _current_app as viz
            if viz is None:
                viz = Imviz()
        except ImportError:
            warnings.warn(
                "`sidecar` would open jdaviz, but it is not installed. To install it, "
                "run `pip install jdaviz`.",
                UserWarning
            )
    if mal is None:
        from mast_aladin_lite.app import gca
        mal = gca()
        if mal is None:
            mal = MastAladin()

    @solara.component
    def Page(viz=viz, mal=mal):
        n_columns = sum(app is not None for app in [viz, mal])

        with solara.Columns(n_columns * [1], gutters_dense=True):
            with solara.Column():
                solara.display(viz.app)
            with solara.Column():
                mal.height = 600
                solara.display(mal)

    with Sidecar(anchor=anchor, title=title):
        solara.display(Page())

    return viz, mal
