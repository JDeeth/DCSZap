from time import sleep


class Script:
    """Parses script text and sends the commands to DCS at specified intervals"""

    def __init__(self, script, dcs_socket=None):
        self._dcs = dcs_socket
        self.name = "(undefined)"
        self.description = "(undefined)"
        self.interval = 0.2
        self.steps = []
        for line in script.splitlines():
            line = " ".join(line.split())
            verb, _, remainder = line.partition(" ")
            if verb == "script":
                self.name = remainder
            elif verb == "description":
                self.description = remainder
            elif verb == "interval":
                self.interval = float(remainder)
            elif verb in ("set", "pause"):
                self.steps.append((verb, remainder))

    @classmethod
    def load(cls, socket, filename):
        with open(filename, encoding="utf_8") as file:
            return Script(file.read(), dcs_socket=socket)

    def run(self):
        """Execute the sequence of steps"""
        for verb, msg in self.steps:
            if verb == "set":
                self._parse_command(msg)
                sleep(self.interval)
            elif verb == "pause":
                delay = float(msg)
                sleep(delay)

    def _parse_command(self, msg):
        """Prepare script line for DCS-BIOS"""
        identifier, _, arg = msg.partition(" ")
        if not arg:
            return
        # if arg represents a float, clamp to 0..1 then map to 0..65535 int
        if "." in arg:
            try:
                arg = max(0.0, min(float(arg), 1.0))
                arg = int(65535 * arg)
            except ValueError:
                # if conversion fails, just send arg as it was written
                pass
        self._dcs.send_cmd(identifier, arg)
