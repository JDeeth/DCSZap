#!/usr/bin/python
import argparse
from dataclasses import dataclass, field
import os
import os.path
import re
import sys
from time import sleep
import socket

__version__ = "0.4.3"
__version_info__ = tuple(
    int(re.match(r"^\d+", i).group()) for i in __version__.split(".")
)


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
    """An instruction in a DCSZap script"""

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


def default_script_dir():
    """in Saved Games Windows folder, or in Example subfolder"""
    user_profile = os.getenv("USERPROFILE")
    if user_profile:
        return os.path.join(user_profile, "Saved Games", "DCSZap")
    return os.path.join(os.curdir, "example")


@dataclass
class AppConfig:
    """Parameters for app to run"""

    host: str = "127.0.0.1"
    port: int = 7778
    script_dir: str = field(default_factory=default_script_dir)
    quiet: bool = False


class App:
    """Show, select and run scripts"""

    def __init__(self, config=AppConfig()):
        self._addr = (config.host, config.port)
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._script_dir = config.script_dir
        self._quiet = config.quiet

    def run(self):
        """Repeatedly prompt to select and run a script"""
        while True:
            print(f"Scripts located in {self._script_dir}:")
            filenames = []
            for filename in os.listdir(self._script_dir):
                full_filename = os.path.join(self._script_dir, filename)
                if os.path.isfile(full_filename) and filename.endswith(".txt"):
                    filenames.append(full_filename)
            for i, filename in enumerate(filenames, start=1):
                script = Script.load(filename)
                print(f"{i:2} {script.name:32}{script.description}")
            try:
                selection = int(input("> ")) - 1
            except (KeyboardInterrupt, ValueError):
                sys.exit()
            if selection not in range(0, len(filenames)):
                continue
            Script.load(filenames[selection]).run(self, self._quiet)
            if not self._quiet:
                print("Script complete!\n")

    def send_cmd(self, identifier, arg):
        """Send command to DCS-BIOS"""
        self._sock.sendto(bytes(f"{identifier} {arg}\n", "utf-8"), self._addr)


def main():
    """Start app"""
    parser = argparse.ArgumentParser(
        description="Send a sequence of commands to DCS-BIOS from a text file",
    )
    parser.add_argument(
        "-v", "--version", action="store_true", help="show version number and exit"
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
        help="DCSZap scripts directory",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="don't print output when running script",
    )
    args = parser.parse_args()
    if args.version:
        print(f"dcszap {__version__}")
        sys.exit()

    app_config = AppConfig(
        host=args.host,
        port=args.port,
        quiet=args.quiet,
    )
    if args.scripts:
        app_config.script_dir = args.scripts

    if not os.path.isdir(app_config.script_dir):
        print(
            f"""\
Error: {app_config.script_dir} is not a directory
Create this directory, or use --scripts to specify a different directory"""
        )
        sys.exit(-1)

    app = App(app_config)
    app.run()


if __name__ == "__main__":
    main()
