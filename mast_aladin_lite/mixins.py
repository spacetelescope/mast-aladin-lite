from functools import wraps


def delay_until_render(function, attr='_wcs'):
    """
    Delay a call on `function` until `attr` updates.
    """

    @wraps(function)
    def wrapper(self, *args, **kwargs):
        """Check if the widget is ready to execute a function.

        Parameters
        ----------
        self : any
            The widget object.
        *args : any
            The arguments of the function.
        **kwargs : any
            The keyword arguments of the function.

        Returns
        -------
        any
            The result of the function if the widget is ready.

        """

        # when the app is first constructed but not shown,
        # `_wcs` is an empty dict, so `rendered` will be False.
        # If `len(_wcs) > 0`, rendered will be True.
        rendered = bool(min(len(getattr(self, attr)), 1))

        def inner_func(change, rendered=rendered):
            # if the app is not rendered:

            if not rendered:
                # On first render, unobserve the traitlet, then call function
                rendered = True
                self.unobserve(inner_func, attr)
                return function(self, *args, **kwargs)

        # on construction and before render, observe the traitlet
        if not rendered:
            self.observe(inner_func, attr)

    return wrapper


class DelayUntilRendered:

    @delay_until_render
    def delayed_add_fits(self, *args, **kwargs):
        self.add_fits(*args, **kwargs)

    @delay_until_render
    def delayed_add_table(self, *args, **kwargs):
        self.add_table(*args, **kwargs)

    @delay_until_render
    def delayed_add_graphic_overlay_from_stcs(self, *args, **kwargs):
        self.add_graphic_overlay_from_stcs(*args, **kwargs)

    @delay_until_render
    def delayed_add_graphic_overlay_from_region(self, *args, **kwargs):
        self.add_graphic_overlay_from_region(*args, **kwargs)
