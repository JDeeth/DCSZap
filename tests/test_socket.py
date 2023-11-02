# pylint: skip-file
import os
from dcszap import App, AppConfig


def test_send_command(mocker):
    mock_socket = mocker.patch("dcszap.socket.socket", autospec=True).return_value

    config = AppConfig(host="192.1.2.3", port=24601, script_dir=os.curdir)
    app = App(config)
    app.send_cmd("PANEL_LIGHTING", 1)

    mock_socket.sendto.assert_called_once_with(
        b"PANEL_LIGHTING 1\n", ("192.1.2.3", 24601)
    )
