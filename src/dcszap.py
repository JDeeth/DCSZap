#!/usr/bin/python
import argparse
from dataclasses import dataclass
import os
import os.path
import sys
from time import sleep
import socket

__version_info__ = (0, 4, 0)
__version__ = ".".join(str(i) for i in __version_info__)


def float_to_65535(arg):
    """If string is a float, map 0..1 to 0..65535 integer"""
    if "." in arg:
        try:
            arg = max(0.0, min(float(arg), 1.0))
            arg = int(65535 * arg)
        except ValueError:
            pass
    return arg


@dataclass(frozen=True)
class Step:
    action: str
    argument: str
    comment: str = ""


class Script:
    """Parses script text and sends the commands to DCS at specified intervals"""

    def __init__(self, script_text):
        self.name = "(undefined)"
        self.description = "(undefined)"
        self.interval = 0.2
        self.steps = []

        for line in script_text.splitlines():
            line, _, comment = (x.strip() for x in line.partition("#"))
            line = " ".join(line.split())
            linetype, _, arg = line.partition(" ")
            if linetype == "script":
                self.name = arg
            elif linetype == "description":
                self.description = arg
            elif linetype == "interval":
                self.interval = float(arg)
            elif linetype in ("set", "pause"):
                self.steps.append(Step(linetype, arg, comment))

    @classmethod
    def load(cls, filename):
        """Load script from file"""
        with open(filename, encoding="utf_8") as file:
            return Script(file.read())

    def run(self, dcs_socket, quiet):
        """Execute the sequence of steps"""
        p = (lambda *a, **kw: None) if quiet else print
        for step in self.steps:
            if step.action == "set":
                identifier, _, arg = step.argument.partition(" ")
                arg = float_to_65535(arg)
                cmt1, _, cmt2 = step.comment.partition(":")
                p(f"{identifier:32}{arg:<16}{cmt1:32}{cmt2}")
                dcs_socket.send_cmd(identifier, arg)
                sleep(self.interval)
            elif step.action == "pause":
                p(f"Pause {step.argument}s")
                sleep(float(step.argument))


class App:
    def __init__(self, host, port, script_dir, quiet):
        self._addr = (host, port)
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if not os.path.exists(script_dir):
            print(f"Error: Scripts directory does not exist: {script_dir}")
            sys.exit()
        self._script_dir = script_dir
        self._quiet = quiet

    def run(self):
        """Repeatedly prompt to select and run a script"""
        while True:
            print(f"Scripts located in {self._script_dir}:")
            scripts = []
            for filename in os.listdir(self._script_dir):
                full_filename = os.path.join(self._script_dir, filename)
                if os.path.isfile(full_filename) and filename.endswith(".txt"):
                    scripts.append(Script.load(full_filename))
            for i, script in enumerate(scripts, start=1):
                print(f"{i:2} {script.name:32}{script.description}")
            try:
                selection = int(input("> ")) - 1
            except (KeyboardInterrupt, ValueError):
                sys.exit()
            if selection not in range(0, len(scripts)):
                continue
            scripts[selection].run(self, self._quiet)
            if not self._quiet:
                print("Script complete!\n")

    def send_cmd(self, identifier, arg):
        """Send command to DCS-BIOS"""
        self._sock.sendto(bytes(f"{identifier} {arg}\n", "utf-8"), self._addr)


def main():
    """Start app"""

    def dir_path(path):
        if not os.path.isdir(path):
            raise argparse.ArgumentTypeError(f"{path} is not a directory")
        return path

    default_dir = os.path.join(os.getenv("USERPROFILE"), "Saved Games", "DCSZap")

    parser = argparse.ArgumentParser(
        description="Send a sequence of commands to DCS-BIOS from a text file"
    )
    parser.add_argument(
        "-a",
        "--host",
        default="127.0.0.1",
        help="computer running DCS",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=7778,
        help="DCS-BIOS port",
    )
    parser.add_argument(
        "-d",
        "--scripts",
        type=dir_path,
        default=default_dir,
        help="DCSZap scripts directory",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="don't print output when running script",
    )
    args = parser.parse_args()
    app = App(
        host=args.host,
        port=args.port,
        script_dir=args.scripts,
        quiet=args.quiet,
    )
    app.run()


if __name__ == "__main__":
    main()
