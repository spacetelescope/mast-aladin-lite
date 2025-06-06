import ipywidgets as widgets
from IPython.display import display

class ViewerSyncUI:
    def __init__(self, sync_manager):
        self.sync_manager = sync_manager
        self.viewer_selector = widgets.Dropdown(
            options=self._get_viewer_options(),
            description='Sync from:',
            layout=widgets.Layout(width='300px')
        )

        self.sync_button = widgets.Button(
            description="Sync Viewers",
            button_style="primary",
            tooltip="Sync all other viewers to the selected viewer"
        )
        self.sync_button.on_click(self._on_sync_clicked)

        self.status_output = widgets.Output()

        self.ui = widgets.VBox([
            self.viewer_selector,
            self.sync_button,
            self.status_output
        ])

    def _get_viewer_options(self):
        return list(self.sync_manager._adapters.keys())

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

    def display(self):
        display(self.ui)