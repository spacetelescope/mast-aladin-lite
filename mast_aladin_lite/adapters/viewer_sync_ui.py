import ipywidgets as widgets
from ipywidgets import Layout
from IPython.display import display

from mast_aladin_lite.adapters import ImvizSyncAdapter, AladinSyncAdapter


class ViewerSyncUI():
    def __init__(self):

        self.mast_aladin_sync_adapter = AladinSyncAdapter()
        self.imviz_sync_adapter = ImvizSyncAdapter()

        # configure the mast aladin sync button
        self.mast_aladin_sync_button = widgets.Button(
            description="Sync to Mast Aladin Viewer",
            button_style="primary",
            tooltip="Sync all other viewers to the Mast Aladin viewer",
            layout=Layout(flex='1 1 auto')
        )
        self.mast_aladin_sync_button.on_click(self._on_sync_to_mast_aladin)

        # configure the imviz sybnc button
        self.imviz_sync_button = widgets.Button(
            description="Sync to Imviz Viewer",
            button_style="primary",
            tooltip="Sync all other viewers to the Imviz viewer",
            layout=Layout(flex='1 1 auto')
        )
        self.imviz_sync_button.on_click(self._on_sync_to_imviz)

        self.status_output = widgets.Output()

        box_layout = Layout(
            display='flex',
            flex_flow='row',
            align_items='stretch',
            width='100%')

        self.sync_buttons = widgets.Box(
            [
                self.imviz_sync_button,
                self.mast_aladin_sync_button,
                self.status_output
            ],
            layout=box_layout)

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
        self.imviz_sync_adapter.sync_to(self.mast_aladin_sync_adapter)

    def _on_sync_to_imviz(self, b):
        self.mast_aladin_sync_adapter.sync_to(self.imviz_sync_adapter)

    def display(self):
        self.imviz_sync_adapter.show()
        display(self.sync_buttons)
        self.mast_aladin_sync_adapter.show()
