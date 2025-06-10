from astropy.coordinates import SkyCoord


class AID:
    """
    Provides API for mast-aladin-lite to allow for parity with
    jdaviz. This is to be used as a mixin within exisiting classes.
    This is based on the Astro Image Display API (AIDA)[1]_.

    References
    ----------
    .. [1] https://github.com/astropy/astro-image-display-api/

    """

    def __init__(self, mast_aladin):
        self.app = mast_aladin

    def set_viewport(self, center):
        """
        Sets the viewport based on provided parameters.
        Presently, centers the viewer on a particular point, `center`,
        given as `~astropy.coordinates.SkyCoord` objects.

        Parameters
        ----------
        center : `~astropy.coordinates.SkyCoord`
            Center the viewer on this coordinate.

        Raises
        ------
        TypeError
            Given coordinates are not provided as SkyCoord.

        """

        if not isinstance(center, SkyCoord):
            raise TypeError(
                "`center` must be a SkyCoord object."
            )

        self.app.target = center
