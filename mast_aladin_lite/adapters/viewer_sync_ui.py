import ipywidgets as widgets
from IPython.display import display

from mast_aladin_lite.adapters import ImvizSyncAdapter, AladinSyncAdapter, SyncManager


class ViewerSyncUI():
    def __init__(self):

        self.mast_aladin = AladinSyncAdapter()
        self.imviz = ImvizSyncAdapter()
        self.sync_manager = SyncManager()

        self.buttons = widgets.ToggleButtons(
            options=['None', 'Imviz', 'Mast Aladin'],
            disabled=False,
            button_style='',
            tooltips=['No Syncing', 'Sync to Imviz', 'Sync to Mast Aladin'],
            style=widgets.ToggleButtonsStyle(button_width="33.1%")
        )

        self.buttons.observe(self._handle_sync)

    def _handle_sync(self, _):
        match self.buttons.index:
            case 0:
                self.sync_manager.stop_real_time_sync()
            case 1:
                self.sync_manager.start_real_time_sync(
                    source=self.imviz,
                    destination=self.mast_aladin
                )
            case 2:
                self.sync_manager.start_real_time_sync(
                    source=self.mast_aladin,
                    destination=self.imviz
                )

    def display(self):
        self.imviz.show()
        display(self.buttons)
        self.mast_aladin.show()
