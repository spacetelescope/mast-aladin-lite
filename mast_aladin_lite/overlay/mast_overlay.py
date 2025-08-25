from enum import Enum


class MastOverlayType(Enum):
    MARKER = "marker"
    CATALOG = "catalog"
    TABLE = "table"
    OVERLAY_REGION = "overlay_region"
    OVERLAY_STCS = "overlay_stcs"


class MastOverlay(dict):
    def __init__(self, overlay_info):
        overlay_type = overlay_info.get("type")
        if overlay_type not in {t.value for t in MastOverlayType}:
            raise ValueError(
                f"Invalid overlay type '{overlay_type}'. "
                f"Must be one of {[t.value for t in MastOverlayType]}."
            )
        super().__init__(overlay_info)

    @property
    def type(self):
        return self.get("type")

    @property
    def options(self):
        return self.get("options")

    @property
    def name(self):
        return self.options.get("name")

    @property
    def data(self):
        ignored = ["type", "options"]
        return {key: value for key, value in self.items() if key not in ignored}
