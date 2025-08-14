from typing import Callable, Iterable, Union

from astropy.table import Table
import pytest
from unittest.mock import Mock
import warnings

from mast_aladin_lite import MastAladin
from ipyaladin.elements.error_shape import EllipseError, CircleError


mast_aladin = MastAladin()


test_stcs_iterables = [
    "CIRCLE ICRS 258.93205686 43.13632863 0.625",
]


@pytest.mark.parametrize("stcs_strings", test_stcs_iterables)
def test_overlayers_dict_add_graphic_overlay_from_stcs_iterables(
    monkeypatch: Callable,
    stcs_strings: Union[Iterable[str], str],
) -> None:
    """Test overlayers_dict overlay info from adding iterable STC-S string(s).

    Parameters
    ----------
    stcs_strings : Union[Iterable[str], str]
        The stcs strings to create region overlay info from.

    """
    test_name = "test"
    mock_send = Mock()
    monkeypatch.setattr(MastAladin, "send", mock_send)
    mast_aladin.add_graphic_overlay_from_stcs(stcs_strings, name=test_name)
    
    assert test_name in mast_aladin._overlays_dict
    assert mast_aladin._overlays_dict[test_name]["type"] == "overlay"
    regions_info = mock_send.call_args[0][0]["regions_infos"]
    assert regions_info == mast_aladin._overlays_dict[test_name]["regions_infos"]
    assert regions_info[0]["infos"]["stcs"] in stcs_strings

    # test handling for an overlay with existing name
    with warnings.catch_warnings(record=True) as w:
        mast_aladin.add_graphic_overlay_from_stcs(stcs_strings, name=test_name)
        assert len(w) == 1
        assert test_name + "_1" in str(w[-1].message)

    assert test_name + "_1" in mast_aladin._overlays_dict
    assert mast_aladin._overlays_dict[test_name + "_1"]["type"] == "overlay"
    regions_info = mock_send.call_args[0][0]["regions_infos"]
    assert regions_info == mast_aladin._overlays_dict[test_name + "_1"]["regions_infos"]
    assert regions_info[0]["infos"]["stcs"] in stcs_strings

    # test handling for overlay with no given name
    mast_aladin.add_graphic_overlay_from_stcs(stcs_strings)

    assert "overlay_python" in mast_aladin._overlays_dict
    assert mast_aladin._overlays_dict["overlay_python"]["type"] == "overlay"
    regions_info = mock_send.call_args[0][0]["regions_infos"]
    assert regions_info == mast_aladin._overlays_dict["overlay_python"]["regions_infos"]
    assert regions_info[0]["infos"]["stcs"] in stcs_strings

    # test removing these overlays, resetting for next functionality check
    mast_aladin.remove_overlay([test_name, test_name + "_1", "overlay_python"])
    assert not mast_aladin._overlays_dict


def test_overlayers_dict_add_table(monkeypatch: Callable) -> None:
    """Test overlayers_dict overlay info from a table."""
    test_name = "test"
    table = Table({"a": [1, 2, 3]})
    table["a"].unit = "deg"
    mock_send = Mock()
    monkeypatch.setattr(MastAladin, "send", mock_send)

    # normal table call
    mast_aladin.add_table(table, name=test_name)
    table_sent_message = mock_send.call_args[0][0]
    assert table_sent_message["event_name"] == "add_table"

    assert test_name in mast_aladin._overlays_dict
    assert mast_aladin._overlays_dict[test_name]["type"] == "table"

    # circle error
    # test handling for an overlay with existing name
    with warnings.catch_warnings(record=True) as w:
        mast_aladin.add_table(
            table,
            shape=CircleError(radius="a", default_shape="cross"),
            color="pink",
            name=test_name,
        )
        assert len(w) == 1
        assert test_name + "_1" in str(w[-1].message)

    table_sent_message = mock_send.call_args[0][0]
    assert table_sent_message["options"]["circle_error"] == {
        "radius": "a",
        "conversion_radius": 1,
    }
    assert table_sent_message["options"]["shape"] == "cross"

    assert test_name + "_1" in mast_aladin._overlays_dict
    assert mast_aladin._overlays_dict[test_name + "_1"]["type"] == "table"
    assert mast_aladin._overlays_dict[test_name + "_1"]["options"]["color"] == "pink"
    assert "circle_error" in mast_aladin._overlays_dict[test_name + "_1"]["options"]

    # ellipse error
    mast_aladin.add_table(table, shape=EllipseError(maj_axis="a", min_axis="a", angle="a"))
    table_sent_message = mock_send.call_args[0][0]
    ellipse_options = {
        "maj_axis": "a",
        "min_axis": "a",
        "angle": "a",
        "conversion_angle": 1,
        "conversion_min_axis": 1,
        "conversion_maj_axis": 1,
    }
    assert table_sent_message["options"]["ellipse_error"] == ellipse_options

    assert "catalog_python" in mast_aladin._overlays_dict
    assert mast_aladin._overlays_dict["catalog_python"]["type"] == "table"

    # test removing these overlays, resetting for next functionality check
    mast_aladin.remove_overlay([test_name, test_name + "_1", "catalog_python"])
    assert not mast_aladin._overlays_dict


test_overlay_names = [
    "overlay",
    ["overlay", "overlay_1", "2MASS"],
    "catalog",
    ["overlay_1", "2MASS"],
]


@pytest.mark.parametrize("overlay_names", test_overlay_names)
def test_remove_overlay(
    monkeypatch: Callable,
    overlay_names: Union[Iterable[str], str],
) -> None:
    """Test proper messages sent for removing overlays using their name string(s).

    Parameters
    ----------
    overlay_names : Union[Iterable[str], str]
        The name strings of overlays.
    """
    mock_send = Mock()
    monkeypatch.setattr(MastAladin, "send", mock_send)

    # generate expected overlays_dict to remove names from
    if type(overlay_names) is str:
        overlay_names_list = [overlay_names]
    else:
        overlay_names_list = overlay_names
    mast_aladin._overlays_dict = {name: {} for name in overlay_names_list}

    mast_aladin.remove_overlay(overlay_names)

    event_name = mock_send.call_args[0][0]["event_name"]
    assert isinstance(event_name, str)
    assert event_name == "remove_overlay"

    name_info = mock_send.call_args[0][0]["overlay_names"]
    assert isinstance(name_info, list)
    assert name_info[0] in overlay_names

    if isinstance(overlay_names, list):
        assert name_info == overlay_names

    # confirm each overlay was removed from the dict as expected
    assert not mast_aladin._overlays_dict

    # try removing non-existent layer to confirm error is raised
    with pytest.raises(
        ValueError,
        match="Cannot remove overlayer `does_not_exist` "
        "since this layer does not exist.",
    ):
        mast_aladin.remove_overlay("does_not_exist")
