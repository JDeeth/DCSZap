# DCSZap

This is a minimal DCS-BIOS client to automate setting aircraft controls from
text files.

With thanks to SlipHavoc for [DCSAutoMate](https://github.com/SlipHavoc/DCSAutoMate), the inspiration for this project.
I wanted to build something more lightweight, which ingests text files rather
than .py scripts, at the expense of not having keyboard input or text-to-speech.

## Installation

1. Install [the FlightPanels/Skunkworks fork of DCS-BIOS](https://github.com/DCS-Skunkworks/dcs-bios)
2. Install [Bort](https://github.com/DCS-Skunkworks/Bort/releases) for writing/editing scripts
3. `git clone https://github.com/jdeeth/dcszap`
4. (recommended) `py -m venv venv` then `venv/Scripts/activate` in `dcszap` directory
5. `py -m pip install .`
6. `dcszap`

This will probably reach a point where I can put it on pypi and there'll be no
need to clone the repo.

At this point, all the app does is turn the Gazelle's panel lights on and off
each time you press Enter.

## Usage

Input will be text files in a simple format:

> ```
> script SA342M_Preflight
> description Gazelle SA342M Preflight
> default_interval 0.3
> set PANEL_LIGHTING 1
> set DASHBOARD_LIGHTING 0.05
> pause 0.8
> set TV_ON_OFF 1
> ```

The first three lines set the name and description for the script, and set the
default interval in seconds between commands.

The remainder of the file is `set` and `pause` commands.

`set` is followed by the DCS-BIOS reference and the value to be set. Values
containing a decimal place will be interpreted as floating point and mapped to
the 0-65535 range. Otherwise the values will be sent as-is.

> `set APPLESAUCE 1` sets it to 1  
> `set APPLESAUCE 1.0` sets it to 65535

This means you can use `-<decrease_by>|+<increase_by>` if the item supports it:
> `set ANTICOLL_INTENSITY +3277` - increase by 3277 / ~5%  
> `set ANTICOLL_INTENSITY -3277` - decrease by 3277 / ~5%

`pause` will set a custom interval, in seconds, between the previous command and
the next. This is instead of, not in addition to, the default interval.

Warning - there's no timer code implemented yet - if run all the commands will
be sent one after another.

## Todo
- implement timer code
- implement UI to load and select scripts manually
- implement data read from DCS-BIOS for selecting and starting scripts...?