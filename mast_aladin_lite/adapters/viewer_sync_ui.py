import ipywidgets as widgets
from IPython.display import display

from mast_aladin_lite.adapters import ImvizSyncAdapter, AladinSyncAdapter
from mast_aladin_lite.app import gca


class ViewerSyncUI:
    def __init__(self):
        # configure the mast aladin sync button
        self.mast_aladin_sync_button = widgets.Button(
            description="Sync to Mast Aladin Viewer",
            button_style="primary",
            tooltip="Sync all other viewers to the Mast Aladin viewer"
        )
        self.mast_aladin_sync_button.on_click(self._on_sync_to_mast_aladin)

        # configure the imviz sybnc button
        self.imviz_sync_button = widgets.Button(
            description="Sync to Imviz Viewer",
            button_style="primary",
            tooltip="Sync all other viewers to the Imviz viewer"
        )
        self.imviz_sync_button.on_click(self._on_sync_to_imviz)

        self.status_output = widgets.Output()

        self.ui = widgets.VBox([
            self.mast_aladin_sync_button,
            self.imviz_sync_button,
            self.status_output
        ])

    def _on_sync_clicked(self, b):
        viewer_id = self.viewer_selector.value
        with self.status_output:
            self.status_output.clear_output()
            print(f"Syncing all viewers to: {viewer_id}")
            try:
                self.sync_manager.sync_to(viewer_id)
                print("Sync successful")
            except Exception as e:
                print(f"Sync failed: {e}")

    def _on_sync_to_mast_aladin(self, b):
        from jdaviz.configs.imviz.helper import _current_app
        ImvizSyncAdapter(_current_app.default_viewer).sync_to(AladinSyncAdapter(gca()))

    def _on_sync_to_imviz(self, b):
        from jdaviz.configs.imviz.helper import _current_app
        AladinSyncAdapter(gca()).sync_to(ImvizSyncAdapter(_current_app.default_viewer))

    def display(self):
        display(self.ui)