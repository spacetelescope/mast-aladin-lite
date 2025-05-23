from ipyaladin import Aladin
from mast_aladin_lite.aida import AID


class MastAladin(Aladin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aid = AID(self)
    
    pass
