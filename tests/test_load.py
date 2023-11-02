# pylint: skip-file
import pytest
from dcszap import AppConfig, Script, Step, App
from tests import arg_or_kwarg

sample_script = """
script SA342M_Preflight
description Gazelle SA342M Preflight
interval 0.3
set PANEL_LIGHTING 1
set DASHBOARD_LIGHTING 0.05
pause 0.8
set TV_ON_OFF 1
"""


def test_load_good_script():
    scr = Script(sample_script)
    assert scr.name == "SA342M_Preflight"
    assert scr.description == "Gazelle SA342M Preflight"
    assert scr.interval == 0.3
    assert scr.steps == [
        Step("set", "PANEL_LIGHTING 1"),
        Step("set", "DASHBOARD_LIGHTING 0.05"),
        Step("pause", "0.8"),
        Step("set", "TV_ON_OFF 1"),
    ]


@pytest.fixture
def app_config():
    return AppConfig(host="192.100.200.300", port=24601, script_dir=".", quiet=True)


def sendto_data(mock_call):
    return arg_or_kwarg(mock_call, 0, "__data")


def test_good_script_makes_correct_calls(mocker, app_config):
    mock_socket = mocker.patch("dcszap.socket.socket", autospec=True).return_value
    mock_sleep = mocker.patch("dcszap.sleep")

    app = App(app_config)
    scr = Script(sample_script)
    scr.run(app, False)

    assert [sendto_data(c) for c in mock_socket.sendto.mock_calls] == [
        b"PANEL_LIGHTING 1\n",
        b"DASHBOARD_LIGHTING 3276\n",
        b"TV_ON_OFF 1\n",
    ]
    assert [sendto_data(c) for c in mock_sleep.mock_calls] == [
        0.3,
        0.3,
        0.8,
        0.3,
    ]


def test_float_conversion(mocker, app_config):
    inpt = """
        set APPLESAUCE 0
        set APPLESAUCE 1
        set APPLESAUCE 0.00
        set APPLESAUCE 0.01
        set APPLESAUCE 0.50
        set APPLESAUCE 0.99
        set APPLESAUCE 1.00
    """
    mock_socket = mocker.patch("dcszap.socket.socket", autospec=True).return_value
    mock_sleep = mocker.patch("dcszap.sleep")

    app = App(app_config)
    scr = Script(inpt)
    scr.run(app, False)

    assert [sendto_data(c) for c in mock_socket.sendto.mock_calls] == [
        b"APPLESAUCE 0\n",
        b"APPLESAUCE 1\n",
        b"APPLESAUCE 0\n",
        b"APPLESAUCE 655\n",
        b"APPLESAUCE 32767\n",
        b"APPLESAUCE 64879\n",
        b"APPLESAUCE 65535\n",
    ]
