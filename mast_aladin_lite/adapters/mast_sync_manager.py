from .viewer_sync_adapter import ViewerSyncAdapter

class MastSyncManager():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._adapters = {}

    def register_viewer(self, viewer_id, adapter: ViewerSyncAdapter):
        self._adapters[viewer_id] = adapter

    def get_adapter(self, viewer_id):
        if viewer_id not in self._adapters:
            raise TypeError(f"No registered ViewerSyncAdapter for viewer id {viewer_id}")
        return self._adapters[viewer_id]

    def sync_to(self, viewer_id):
        sync_adapter = self.get_adapter(viewer_id)
        for id, adapter in self._adapters.items():
            if id != viewer_id:
                adapter.sync_to(sync_adapter)

