import os
import os.path
import sys
from dcs_bios_socket import DcsBiosSocket
from script import Script

__version_info__ = (0, 2, 0)
__version__ = ".".join(str(i) for i in __version_info__)


def main():
    """Connect to DCS, select and load scripts"""
    addr = "127.0.0.1"
    port = 7778
    addr = input(f"DCS IP address [{addr}]: ") or addr
    port = input(f"DCS-BIOS port [{port}]: ") or port
    dcs_socket = DcsBiosSocket(addr, port)

    script_dir = os.path.join(os.getenv("USERPROFILE"), "Saved Games", "DCSZap")
    try:
        os.makedirs(script_dir)
    except OSError:
        pass

    while True:
        print(f"Scripts located in {script_dir}:")
        scripts = []
        for filename in os.listdir(script_dir):
            full_filename = os.path.join(script_dir, filename)
            if os.path.isfile(full_filename) and filename.endswith(".txt"):
                scripts.append(Script.load(dcs_socket, full_filename))
        for i, script in enumerate(scripts, start=1):
            print(f"{i:2} {script.name:32}{script.description}")
        try:
            selection = int(input("> ")) - 1
        except (KeyboardInterrupt, ValueError):
            sys.exit()
        if selection >= len(scripts):
            continue
        scripts[selection].run()
        print("Script complete!\n")
