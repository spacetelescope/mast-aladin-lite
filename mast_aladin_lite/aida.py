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

    def set_viewport(self, center=None, fov=None):
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

        Raises
        ------
        TypeError
            Given coordinates are not provided as SkyCoord.

        """

        if center is not None:
            if not isinstance(center, SkyCoord):
                raise TypeError(
                    "`center` must be a SkyCoord object."
                )

            self.app.target = center

        if fov is not None:
            scale_factor = 0
            if isinstance(fov, (u.Quantity, Angle)):
                fov = fov.value

            elif not isinstance(fov, (float, int)):
                raise ValueError(
                    f"`fov` must be an `~astropy.coordinates.Angle` or float, got {fov=}"
                )

            current_fov = self.app.fov.to_value(u.deg)
            aspect_ratio = float(self.app._fov_xy["y"] / self.app._fov_xy["x"])

            # Determine the scale factor by which we want to adjust setting the
            # ipyaladin horizontal fov
            if aspect_ratio > 1:
                scale_factor = float(fov / current_fov)
            else:
                scale_factor = float(fov / self.app._fov_xy["y"])

            self.app.fov = self.app.fov * scale_factor

    def get_viewport(
        self, sky_or_pixel="sky", image_label=None
    ):
        """
        Gets the viewport center and field of view.

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
                An object representing the field of view of the shorter axis.
            - image_label: None
                A string representing the label of the image, always `None`
                for aladin-lite.

        Raises
        ------
        NotImplementedError
            Given `sky_or_pixel` is not "sky" or `None`.
            Given `image_label` is not `None`.

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

        aspect_ratio = float(self.app._fov_xy["y"]/self.app._fov_xy["x"])
        if aspect_ratio > 1:
            current_fov = self.app._fov_xy["x"]
        else:
            current_fov = self.app._fov_xy["y"]

        viewport_state = dict(
            center=self.app.target,
            fov=current_fov,
            image_label=None
        )

        return viewport_state
