from ipyaladin import Aladin
from mast_aladin_lite.aida import AID


# store reference to the latest instantiation:
_latest_instantiated_app = None


class MastAladin(Aladin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aid = AID(self)

        global _latest_instantiated_app
        _latest_instantiated_app = self


def gca():
    """
    Get the current mast-aladin-lite application instance.

    Returns
    -------
    MastAladin
    """
    return _latest_instantiated_app
