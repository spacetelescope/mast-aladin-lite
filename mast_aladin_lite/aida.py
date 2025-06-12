from astropy.coordinates import SkyCoord
from typing import Any


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

    def get_viewport(
            self, sky_or_pixel: str | None = "sky", image_label: str | None = None) -> dict[str, Any]:
        """
        Gets the current viewport of the viewer.
        Presently, returns a dictionary containing the viewer's `center`,
        given as `~astropy.coordinates.SkyCoord` objects, and the viewer's
        `fov`, given as an `~astropy.units.Angle` object.

        Parameters
        ----------
        sky_or_pixel : str, optional
            If 'sky', the center will be returned as a `SkyCoord` object.
            If `None`, the default behavior is to return the center as a `SkyCoord`.
            Any other values will raise the error that "aladin-lite is a HiPS viewer
            without a concept of pixels"
        image_label : str, optional
            The label of the image to get the viewport for. If a value is provided,
            the error will be raised that "aladin-lite only shows one 'image' per
            viewer, and does not need the concept of labels”.

        Returns
        -------
        dict
            A dictionary containing:
            - center : `~astropy.coordinates.SkyCoord`
                Center the viewer on this coordinate.
            - fov : `~astropy.coordinates.Angle`
                An object representing the field of view.

        Raises
        ------
        TypeError
            Given coordinates are not provided as SkyCoord.

        """

        viewport_state = {}

        if sky_or_pixel != "sky" and sky_or_pixel is not None:
            raise NotImplementedError(
                "aladin-lite is a HiPS viewer without a concept of pixels. `sky_or_pixel` must be set to 'sky' or `None`"
            )

        if image_label is not None:
            raise NotImplementedError(
                "aladin-lite only shows one 'image' per viewer, and does not need the concept of labels. `image_label` must be set to `None`."
            )

        viewport_state["center"] = self.app.target
        viewport_state["fov"] = self.app.fov

        return viewport_state
