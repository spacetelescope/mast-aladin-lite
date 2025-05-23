from astropy.coordinates import SkyCoord

class AID:
    """
    Provides API for mast-aladin-lite to allow for parity with 
    jdaviz. This is to be used as a mixin within exisiting classes.
    This is based on the Astro Image Display API (AIDA) formerly known
    as the astrowidgets API.

    """

    # __init__ the basics
    def __init__(self, mast_aladin):
        self.app = mast_aladin

    def center_on(self, point):
        """
        Centers the viewer on a particular point given as SkyCoords. 

        Parameters
        ----------
        point : `~astropy.coordinates.SkyCoord`

        Raises
        ------
        NotImplementedError
            Given coordinates are not provided as SkyCoord.

        """
        # add check the coords are instance of sky coords, raise warning if not
        # common APIs method only takes center on

        if not isinstance(point, SkyCoord):
            raise NotImplementedError
        
        self.app.target = point
        