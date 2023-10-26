# pylint: skip-file

from mock import call
from script import Script
from dcs_bios_socket import DcsBiosSocket


sample_script = """
script SA342M_Preflight
description Gazelle SA342M Preflight
default_interval 0.3
set PANEL_LIGHTING 1
set DASHBOARD_LIGHTING 0.05
pause 0.8
set TV_ON_OFF 1
"""


def test_load_good_script():
    scr = Script(sample_script)
    assert scr.name == "SA342M_Preflight"
    assert scr.description == "Gazelle SA342M Preflight"
    assert scr.default_interval == 0.3
    assert scr.steps == [
        ("set", "PANEL_LIGHTING 1"),
        ("set", "DASHBOARD_LIGHTING 0.05"),
        ("pause", "0.8"),
        ("set", "TV_ON_OFF 1"),
    ]


def test_wtf():
    c = call("asdf", 234)
    assert c.args[0] == "asdf"


def test_good_script_makes_correct_calls(mocker):
    mock_socket = mocker.patch(
        "dcs_bios_socket.socket.socket", autospec=True
    ).return_value

    scr = Script(sample_script, DcsBiosSocket())
    scr.run()

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
    mock_socket = mocker.patch(
        "dcs_bios_socket.socket.socket", autospec=True
    ).return_value

    scr = Script(inpt, DcsBiosSocket())
    scr.run()

    assert [c.args[0] for c in mock_socket.sendto.mock_calls] == [
        b"APPLESAUCE 0\n",
        b"APPLESAUCE 1\n",
        b"APPLESAUCE 0\n",
        b"APPLESAUCE 655\n",
        b"APPLESAUCE 32767\n",
        b"APPLESAUCE 64879\n",
        b"APPLESAUCE 65535\n",
    ]
