import socket


class DcsBiosSocket:
    """Wrapper for socket connection to DCS-BIOS"""

    def __init__(self, addr="127.0.0.1", port=7778):
        self._addr = addr
        self._port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_cmd(self, identifier, arg):
        """Send command to DCS-BIOS"""
        self._sock.sendto(
            bytes(f"{identifier} {arg}\n", "utf-8"),
            (self._addr, self._port),
        )
