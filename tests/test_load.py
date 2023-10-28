# pylint: skip-file

from dcszap import Script, Step, App
import os

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


def test_good_script_makes_correct_calls(mocker):
    mock_socket = mocker.patch("dcszap.socket.socket", autospec=True).return_value

    app = App("192.100.200.300", 24601, os.curdir, True)
    scr = Script(sample_script)
    scr.run(app, False)

    assert [c.args[0] for c in mock_socket.sendto.mock_calls] == [
        b"PANEL_LIGHTING 1\n",
        b"DASHBOARD_LIGHTING 3276\n",
        b"TV_ON_OFF 1\n",
    ]


def test_float_conversion(mocker):
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

    app = App("192.100.200.300", 24601, os.curdir, True)
    scr = Script(inpt)
    scr.run(app, False)

    assert [c.args[0] for c in mock_socket.sendto.mock_calls] == [
        b"APPLESAUCE 0\n",
        b"APPLESAUCE 1\n",
        b"APPLESAUCE 0\n",
        b"APPLESAUCE 655\n",
        b"APPLESAUCE 32767\n",
        b"APPLESAUCE 64879\n",
        b"APPLESAUCE 65535\n",
    ]
