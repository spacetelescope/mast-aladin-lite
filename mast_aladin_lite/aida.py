from astropy.coordinates import SkyCoord, Angle
import astropy.units as u


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

    def _set_center(self, center=None):
        if center is None:
            return

        if not isinstance(center, SkyCoord):
            raise TypeError(
                "`center` must be a SkyCoord object."
            )

        self.app.target = center

    def _set_fov(self, fov=None):
        if fov is None:
            return

        if isinstance(fov, (u.Quantity, Angle)):
            fov = fov.to_value(u.deg)

        elif not isinstance(fov, (float, int)):
            raise ValueError(
                f"`fov` must be an `~astropy.coordinates.Angle` or float, got {fov=}"
            )

        # Determine the scale factor by which we want to adjust setting the
        # ipyaladin horizontal fov
        scale_factor = fov / min(self.app.fov_xy).to_value(u.deg)
        self.app.fov = self.app.fov * scale_factor

    def _set_rotation(self, rotation=None):
        if rotation is None:
            return

        if not isinstance(rotation, (Angle)) and not isinstance(rotation, float):
            raise TypeError(
                "`rotation` must be an `~astropy.coordinates.Angle` or float."
            )

        if isinstance(rotation, (u.Quantity, Angle)):
            rotation = rotation.to_value(u.deg)        
        
        self.app.rotation = rotation

    def set_viewport(self, center=None, fov=None, rotation=None, image_label=None, **kwargs):
        """
        Sets the viewport based on provided parameters.
        Presently, centers the viewer on a particular point, `center`,
        given as `~astropy.coordinates.SkyCoord` objects.

        Parameters
        ----------
        center : `~astropy.coordinates.SkyCoord`
            Center the viewer on this coordinate.
        fov : `~astropy.coordinates.Angle` or float
            Set the length of the viewport's smaller axis to span `fov`, as an
            `~astropy.coordinates.Angle` or as a float in units of degrees.
        rotation : `~astropy.coordinates.Angle`, float
            Set the angle between "+y" or "up" in the viewport and north in
            degrees east of north (counter-clockwise). It can be set with
            an `~astropy.coordinates.Angle` or floats interpreted
            as angles in units of degrees.

        Raises
        ------
        TypeError
            - Given coordinates are not provided as SkyCoord.
            - Given fov is not provided as Angle or float.
            - Given rotation is not provided as Angle or float.

        """

        self._set_center(center)
        self._set_fov(fov)
        self._set_rotation(rotation)

    def get_viewport(
        self, sky_or_pixel="sky", image_label=None
    ):
        """
        Gets the viewport center, field of view, and rotation.

        Parameters
        ----------
        sky_or_pixel : str, optional
            If `"sky"` or `None`, the viewport center and field of view will be returned
            in world coordinates. `"pixel"` is not supported for HiPS viewers.
        image_label : str, optional
            `image_label` is a required argument for ``AID`` API compatibility,
            but it is not relevant for HiPS browsers like aladin-lite. If not
            `None`, an error will be raised.

        Returns
        -------
        dict
            A dictionary containing:
            - center : `~astropy.coordinates.SkyCoord`
                Center the viewer on this coordinate.
            - fov : `~astropy.coordinates.Angle`
                The length of the shorter viewport axis.
            - rotation : `~astropy.coordinates.Angle`
                Angle of the view center to north pole angle in degrees.
            - image_label: None
                A string representing the label of the image, always `None`
                for aladin-lite.

        Raises
        ------
        NotImplementedError
            - Given `sky_or_pixel` is not "sky" or `None`.
            - Given `image_label` is not `None`.

        """

        if sky_or_pixel != "sky" and sky_or_pixel is not None:
            raise NotImplementedError(
                "aladin-lite is a HiPS viewer without a concept of pixels."
                "`sky_or_pixel` must be set to 'sky' or `None`"
            )

        if image_label is not None:
            raise NotImplementedError(
                "aladin-lite only shows one 'image' per viewer, and does not need"
                "the concept of labels. `image_label` must be set to `None`."
            )

        viewport_state = dict(
            center=self.app.target,
            fov=min(self.app.fov_xy),
            rotation=self.app.rotation,
            image_label=None
        )

        return viewport_state
