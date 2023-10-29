# DCSZap

This is a minimal DCS-BIOS client to automate setting aircraft controls from
text files.

## Installation

1. Install any recent Python 3 version (3.7 or later)
2. Install [the FlightPanels/Skunkworks fork of DCS-BIOS](https://github.com/DCS-Skunkworks/dcs-bios)
3. Download [Bort](https://github.com/DCS-Skunkworks/Bort/releases) to assist with writing your own scripts
4. Clone/download this repository
5. `py ./dcszap.py --scripts ./example`

Or:

4. Clone/download this repository
5. `py -m pip install .` within the directory
6. `dcszap --scripts ./example`

## Usage

DCSZap looks for scripts in `(your user directory)/Saved Games/DCSZap` by
default. You can specify a different directory:
```
dcszap --scripts your/scripts/directory
```

You then select the script by number:
```
$ dcszap
Scripts located in C:/users/Joe Bloggs/Saved Games/DCSZap:
 1 Mi8_Preflight                   Mi-8 preflight
 2 Mi8_ArmGunpods                  Mi-8 set up gunpods
 3 SA342M_Preflight                Gazelle SA342M preflight
> 3
```

If DCS is running on a different computer, or if DCS-BIOS isn't using port 7778:
```
dcszap --host 192.168.123.45 --port 24601
```

## Scripts

Scripts are text files:

```
script SA342M_Preflight
description Gazelle SA342M Preflight
interval 0.3

set PANEL_LIGHTING 1            # Instrument backlighting: ON
set DASHBOARD_LIGHTING 0.05     # Instrument backlighting: Adjust to 5%
pause 0.8
set TV_ON_OFF 1                 # Viviane TV: On
```


The first lines set the name and description for the script, and optionally the
interval between commands in seconds. If not specified, the interval is 0.2
seconds.

The remainder of the file is `set` and `pause` commands.

`set` is followed by a DCS-BIOS identifier and the argument to be sent.

If the argument contains a decimal place and can be converted into a floating-
point number, it will be mapped to the 0..65535 integer range:

```
set SOME_IDENTIFIER 0.0 # sends SOME_IDENTIFIER 0
set SOME_IDENTIFIER 0.5 # sends SOME_IDENTIFIER 32767
set SOME_IDENTIFIER 1.0 # sends SOME_IDENTIFIER 65535
```
Numbers outside the 0.0 to 1.0 range will be clamped to 0.0 to 1.0:
```
set SOME_IDENTIFIER -2.0 # sends SOME_IDENTIFIER 0
set SOME_IDENTIFIER 42.5 # sends SOME_IDENTIFIER 65535
```
Otherwise the argument is sent exactly as written.
```
set SOME_IDENTIFIER 0
set SOME_IDENTIFIER 1
set SOME_IDENTIFIER +42
set SOME_IDENTIFIER INC
```

`pause` adds a delay between two actions, in addition to the normal interval.

Lines which don't begin with `script`, `description`, `interval`, `set` or `pause`
are ignored and can be used for comments.

End-of-line comments start with `#` and are displayed when the script runs.

## Contributing

If you've written a DCSZap script and you'd like it to be included as an
example, please let me know (via an issue, pull request, Discord, or forum)
and I'd be delighted to include it with attribution.

Ideas, bugfixes, pull requests etc are all welcome too, preferably via GitHub.

## Next steps

- command line option to specify a specific script rather than select from directory
- 2-way comms with DCS-BIOS to, e.g., select a script automatically on loading
  a module, start scripts from within DCS…

## Related projects

With thanks to SlipHavoc for [DCSAutoMate](https://github.com/SlipHavoc/DCSAutoMate), the inspiration for this project.
DCSAutoMate includes the ability to simulate keypresses to carry out actions
unavailable via DCS-BIOS, and is driven from Python scripts, which gives a
great deal of additional flexibility. I wanted to make a system which is more
lightweight, which can be installed and run without much Python expertise and
without using auto-py-to-exe.
