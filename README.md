# DCSZap

This is a minimal DCS-BIOS client to automate setting aircraft controls from
text files.

With thanks to SlipHavoc for [DCSAutoMate](https://github.com/SlipHavoc/DCSAutoMate), the inspiration for this project.
I wanted to build something more lightweight, which ingests text files rather
than .py scripts, at the expense of not having keyboard input or text-to-speech.

## Installation

1. Install [the FlightPanels/Skunkworks fork of DCS-BIOS](https://github.com/DCS-Skunkworks/dcs-bios)
2. Install [Bort](https://github.com/DCS-Skunkworks/Bort/releases) for writing/editing your own scripts
3. `git clone https://github.com/jdeeth/dcszap`
4. (recommended) `py -m venv venv` then `venv/Scripts/activate` in `dcszap` directory
5. `py -m pip install .`
6. Create/copy scripts into `(your user directory)/Saved Games/DCSZap`
7. `dcszap`

## Usage

This app looks for text files in `(your user directory)/Saved Games/DCSZap`

Scripts are in a simple format:

> ```
> script SA342M_Preflight
> description Gazelle SA342M Preflight
> interval 0.3
>
> set PANEL_LIGHTING 1
> set DASHBOARD_LIGHTING 0.05
> pause 0.8
> set TV_ON_OFF 1
> ```

The first lines set the name and description for the script, and optionally the
interval between commands in seconds. If not specified, the interval is 0.2
seconds.

The remainder of the file is `set` and `pause` commands.

`set` is followed by a DCS-BIOS identifier and the argument to be sent.

If the argument contains a decimal place and can be converted into a floating-
point number, it will be mapped to the 0..65535 integer range:

```
set APPLESAUCE 0.0 # sends APPLESAUCE 0
set APPLESAUCE 0.5 # sends APPLESAUCE 32767
set APPLESAUCE 1.0 # sends APPLESAUCE 65535
```
Otherwise the argument is sent as written.
```
set APPLESAUCE 0
set APPLESAUCE 1
set APPLESAUCE +42
set APPLESAUCE INC
```

`pause` adds a delay between two actions, in addition to the normal interval.

Lines which don't begin with `script`, `description`, `interval`, `set` or `pause`
are ignore and can be used for comments.

## Next steps

- reorganise into a single .py file
- publish on pypi
- support for end-of-line comments
- verbose mode
- config file/command line arguments for address, port, scripts folder, etc
