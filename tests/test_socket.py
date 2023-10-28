# pylint: skip-file
import os
from dcszap import App


def test_send_command(mocker):
    mock_socket = mocker.patch("dcszap.socket.socket", autospec=True).return_value

    app = App("192.1.2.3", 24601, os.curdir)
    app.send_cmd("PANEL_LIGHTING", 1)

    mock_socket.sendto.assert_called_once_with(
        b"PANEL_LIGHTING 1\n", ("192.1.2.3", 24601)
    )
