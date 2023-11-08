# DCSZap

This is a minimal DCS-BIOS client to automate setting aircraft controls from
text files.

Version 0.4.3

## Installation

1. Install any recent Python 3 version (3.7 or later)
2. Install [the FlightPanels/Skunkworks fork of DCS-BIOS](https://github.com/DCS-Skunkworks/dcs-bios)
3. Download [Bort](https://github.com/DCS-Skunkworks/Bort/releases) to assist with writing your own scripts
4. Copy the [example script](https://github.com/JDeeth/DCSZap/tree/main/example)  to `%USERPROFILE%/Saved Games/DCSZap` - create this folder alongside your DCS settings folder
5. From the command prompt/terminal:
    ```
    pip install dcszap
    ```

## Usage

From the command prompt/terminal:
```
dcszap
```

You will be given a list of scripts (`.txt` files in the scripts directory):
```
$ dcszap
Scripts located in C:/Users/YourNameHere/Saved Games/DCSZap:
 1 Mi8_Preflight                   Mi-8 preflight
 2 Mi8_ArmGunpods                  Mi-8 set up gunpods
 3 SA342M_Preflight                Gazelle SA342M preflight
>
```
Type the number of the script you want to run and press Enter to run.

The commands are sent to DCS-BIOS over a network socket - the DCS window
does not need to be in focus for the scripts to work. Some modules may
require you to be in the aircraft cockpit.

You'll see the commands on the screen as they run:
```
> 3
TABLET_PW                   TOGGLE          Tablet                       Off
TABLET_SHOW                 TOGGLE          Tablet                       Stow
PANEL_LIGHTING              1               Panel lighting               On
DASHBOARD_LIGHTING          3276            Backlight brightness         Set 5%
...
FLARE_DISP_FIRE_CAP         1               Flare dispense switch cover  Open
WEAPONS_MASTER_ARM          1               Master arm                   On
ANTICOLL_LIGHTS             1               Anticollision lights         Off
Script complete!
```
You can then start another script. Enter nothing or `Ctrl-C` to quit.

## Options

To use scripts stored in a location other than `%USERPROFILE%/Saved Games/DCSZap`:
```
dcszap --scripts your/scripts/directory
```

If DCS is running on a different computer, or if DCS-BIOS isn't using port 7778:
```
dcszap --host 192.168.123.45 --port 24601
```

To suppress messages while the script is running:
```
dcszap --quiet
```

For a full description:
```
dcszap --help
```

## Scripts

Scripts are text files:
```
script SA342M_Preflight
description Gazelle SA342M Preflight
interval 0.3

set PANEL_LIGHTING 1            # Instrument backlighting: On
set DASHBOARD_LIGHTING 0.05     # Backlight brightness: Set 5%
pause 0.8
set TV_ON_OFF 1                 # Viviane TV: On
```

The first lines set the name and description for the script, and optionally the
interval between commands in seconds. If not specified, the interval is 0.2
seconds.

The remainder of the file is `set` and `pause` commands and comments.

`set` is for sending DCS-BIOS commands:
```
set PANEL_LIGHTING 1
```
This sends the argument `1` to the DCS-BIOS identifier `PANEL_LIGHTING` - which
in the Gazelle turns on the instrument backlighting.

End-of-line comments start with `#`. The script will split the comment on `:`
and display them in two columns.

Arguments that look like floating-point numbers - `0.25` say - are converted
into an integer between 0 and 65535. `0.0` becomes 0 and `1.0` becomes 65535.

`pause` adds a delay between two actions, in addition to the normal interval.

Lines which don't begin with `script`, `description`, `interval`, `set` or `pause`
are ignored and can be used for comments.

## Writing scripts

 - Launch your favourite DCS module
 - Open Bort
 - Find the controls you always find yourself using at the start of every flight
 - Operate the controls in DCS and see the values change in Bort
 - Operate the controls in Bort and see them move in DCS
 - Write the control identifiers and the desired values into your own script file (a `.txt` file in the DCSZap scripts folder)
 - Optionally include comments to describe the intent, e.g. that setting the radar alt bug to 2215 corresponds to 10 meters.
 - Save your script and run `dcszap`
 - Run your script
 - See the controls move!

For controls like instrument brightness knobs which take a number between
0 and 65535 representing 0% to 100%, you can enter the value as a floating
point number. DCSZap converts these into into integers - `0.0` to `0`, `1.0`
to `65535`.

To reload the list, enter a number that doesn't correspond to any script e.g. 0.

For more guidance on DCS-BIOS commands, please see:
- [the DCS-BIOS documentation](https://github.com/DCS-Skunkworks/dcs-bios/blob/master/Scripts/DCS-BIOS/doc/developerguide.adoc#the-dcs-bios-import-protocol)
- [the DCS-BIOS source code for the aircraft module](https://github.com/DCS-Skunkworks/dcs-bios/tree/master/Scripts/DCS-BIOS/lib/modules/aircraft_modules)
- [the DCS-BIOS Module Lua class](https://github.com/DCS-Skunkworks/dcs-bios/blob/master/Scripts/DCS-BIOS/lib/modules/Module.lua)

## Contributing

If you'd like your script to be included as an example, please let me know
(via an issue, pull request, Discord, or forum) and I'd be delighted to
include it with attribution. Ideas, bugfixes, pull requests etc are all welcome too.

## Next steps

This project is likely to develop rapidly and the script format could change
in the near future. In particular I'd like to go further with expressing
scripts in human language e.g. `Landing lights: Extend` rather than
`set LANDING_LIGHT 2`, with a translation layer between how the controls are
labelled to the virtual pilot and the identifiers and values used in DCS-BIOS.

- command line option to specify a specific script rather than select from directory, allowing the script to run completely silent
- more obvious selection list reload action
- Make the tests better, largely for the sake of better tests
- 2-way comms with DCS-BIOS to, e.g., select a script automatically on loading
  a module, start scripts from within DCS…
- more example scripts!

## Related projects

With thanks to SlipHavoc for [DCSAutoMate](https://github.com/SlipHavoc/DCSAutoMate), the inspiration for this project.
DCSAutoMate includes the ability to simulate keypresses to carry out actions
unavailable via DCS-BIOS, and is driven from Python scripts, which gives a
great deal of additional flexibility. I wanted to make a system which is more
lightweight, which can be installed and run without auto-py-to-exe or much
Python expertise.
