import solara
import warnings
from ipyaladin import Aladin
from sidecar import Sidecar as UpstreamSidecar

from mast_aladin_lite.app import MastAladin, gca

__all__ = [
    'sidecar'
]

opened_sidecars = []


class sidecar:
    loaded_apps = []
    _sidecar_context = None

    @classmethod
    def open(
        cls,
        *apps,
        anchor='split-bottom',
        use_current_apps=False,
        title='mast-aladin-lite & jdaviz',
        include_aladin=True,
        include_jdaviz=True,
        close_existing=True,
    ):

        """
        Open ``apps`` in a sidecar [1]_. If none are given and
        ``include_aladin`` and ``include_jdaviz`` are `True`,
        open a sidecar with one of each.

        Parameters
        ----------
        anchor : str, optional (default is `'split-bottom'`)
            One of the anchor location options available from
            ``jupyterlab-sidecar``, which include:

                {'split-right', 'split-left', 'split-top',
                 'split-bottom', 'tab-before', 'tab-after',
                 'right'}

        use_current_apps : bool, optional (default is `False`)
            If `True`, get the last constructed Imviz and
            mast-aladin-lite instances to open in the sidecar

        title : str, optional (default is 'mast-aladin-lite & jdaviz')
            Title to appear in the tab label for the sidecar in
            jupyterlab.

        include_aladin : bool, optional (default is `True`)
            The sidecar must include at least one
            mast-aladin-lite instance. If none are already
            available, a new one will be created.

        include_jdaviz : bool, optional (default is `True`)
            The sidecar must include at least one
            jdaviz instance. If none are already available,
            a new one will be created.

        close_existing : bool, optional (default is `True`)
            Close existing sidecar(s) before opening a new one.

        References
        ----------
        .. [1] https://github.com/jupyter-widgets/jupyterlab-sidecar
        """
        # initialize the object here:
        self = cls()

        # This must be run first because we don't have the ability to close multiple
        # sidecars without possibly closing all widgets
        if close_existing:
            cls.close_all()

        apps = list(apps)
        mal_instances = [app for app in apps if isinstance(app, Aladin)]
        jdaviz_instances = []

        if not len(mal_instances) and include_aladin:
            mal = gca()
            if not use_current_apps or (use_current_apps and mal is None):
                mal = MastAladin()
            apps.append(mal)

        try:
            from jdaviz.core.helpers import ConfigHelper
            from jdaviz.configs.imviz.helper import Imviz, _current_app as viz

            jdaviz_instances = [app for app in apps if isinstance(app, ConfigHelper)]

            # construct new imviz if not using current app or no current app exists:
            if not len(jdaviz_instances) and include_jdaviz:
                if not use_current_apps or (use_current_apps and viz is None):
                    viz = Imviz()
                apps.append(viz)

        except ImportError:
            warnings.warn(
                "`sidecar` would open jdaviz, but it is not installed. To install it, "
                "run `pip install jdaviz`.",
                UserWarning
            )

        n_columns = len(apps)

        if not n_columns:
            raise ValueError("No apps to show in sidecar.")

        self.loaded_apps = apps

        @solara.component
        def SidecarContents(n_columns=n_columns):
            # create layout with `n_columns` equal width columns
            with solara.Columns(n_columns * [1], gutters_dense=True):

                for app in apps:
                    if isinstance(app, Aladin):
                        # MastAladin:
                        with solara.Column():
                            app.height = 600
                            solara.display(app)
                    elif app.__class__.__name__.endswith('viz'):
                        # jdaviz:
                        with solara.Column():
                            solara.display(app.app)
                    else:
                        # other:
                        with solara.Column():
                            solara.display(app)

        self._sidecar_context = UpstreamSidecar(anchor=anchor, title=title)
        with self._sidecar_context:
            solara.display(SidecarContents())

        opened_sidecars.append(self)
        return tuple(apps)

    def close(self):
        """
        Close this particular `sidecar` instance.
        """
        # close jdaviz apps within the sidecar:
        for app in sidecar.loaded_apps:
            if app.__class__.__name__.endswith('viz'):
                app.app.close()

        # now close sidecar(s):
        if self._sidecar_context is not None:
            self._sidecar_context.close()

    @classmethod
    def close_all(cls):
        """
        Close all `sidecar` instances.
        """
        while len(opened_sidecars):
            sidecar = opened_sidecars.pop()
            sidecar.close()
