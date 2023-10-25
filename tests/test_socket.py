# pylint: skip-file
import dcszap


def test_send_command(mocker):
    mock_socket = mocker.patch("dcszap.socket.socket", autospec=True).return_value

    db = dcszap.DcsBiosSocket("192.1.2.3", 24601)
    db.send_cmd("PANEL_LIGHTING", 1)

    mock_socket.sendto.assert_called_once_with(
        b"PANEL_LIGHTING 1\n", ("192.1.2.3", 24601)
    )
