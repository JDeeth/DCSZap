class Script:
    def __init__(self, script, dcs_socket=None):
        self._dcs = dcs_socket
        self.name = "(undefined)"
        self.description = "(undefined)"
        self.default_interval = 0.2
        self.steps = []
        for line in script.splitlines():
            line = " ".join(line.split())
            verb, _, remainder = line.partition(" ")
            if verb == "script":
                self.name = remainder
            elif verb == "description":
                self.description = remainder
            elif verb == "default_interval":
                self.default_interval = float(remainder)
            elif verb in ("set", "pause"):
                self.steps.append((verb, remainder))

    def run(self):
        """Execute the sequence of steps. Do not use yet - timer not implemented"""
        for verb, msg in self.steps:
            if verb != "set":
                continue
            ref, space, val = msg.partition(" ")
            if not space:
                continue
            if "." in val:
                try:
                    val = int(65535 * float(val))
                except ValueError:
                    continue
            self._dcs.send_cmd(ref, val)
