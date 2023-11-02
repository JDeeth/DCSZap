# pylint: skip-file
import os
from dcszap import AppConfig


def test_default_path_with_userprofile(monkeypatch):
    monkeypatch.setenv("USERPROFILE", "C:\\Users\\Snoopy")
    ac = AppConfig()
    assert ac.script_dir == os.path.join(
        "C:\\", "Users", "Snoopy", "Saved Games", "DCSZap"
    )


def test_default_path_without_userprofile(monkeypatch):
    monkeypatch.delenv("USERPROFILE")
    ac = AppConfig()
    assert ac.script_dir == os.path.join(os.curdir, "example")
