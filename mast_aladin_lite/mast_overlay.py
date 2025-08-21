class MastOverlay(dict):
    def __init__(self, overlay_info):
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
