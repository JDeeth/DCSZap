# DCSZap

This is a minimal DCS-BIOS client to automate setting aircraft controls from
TOML scripts.

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

## Misc

Gazelle M preflight:

"TABLET_PW", 1, "Tablet: Off"
"TABLET_SHOW", 1, "Tablet: Stow"
"PANEL_LIGHTING", 1, "Panel lighting: Marche"
"DASHBOARD_LIGHTING", int16(0.05), "Dashboard lighting: Adjust"
"UV_LIGHTING", int16(0.40), "UV lighting: Adjust"
"NADIR_ON_OFF_BRIGHTNESS", int16(0.05), "NADIR lighting: Adjust"
"HA_SOURCE", 3, "Flight director source: DOP"
"FLARE_DISPENSER_OFF_ON", 1, "Flare Dispenser: VitE"
"HOT3_PANEL_TEST_OFF_ON", 3, "HOT3 weapon key: JOUR"
"HOT3_BRIGHTNESS", int16(0.05), "HOT3 brightness: Adjust"
"HOT3_STATION_SELECT", 1, "HOT3 station select: 1"
"LASER_POWER", 1, "BCV (video box) power: Marche"
"CTH_POWER", 2, "CTH (thermal camera) power: Marche"
"TV_ON_OFF", 1, "TV: On"
"RWR_BRIGHTNESS", int16(0.03), "RWR brightness: Adjust"
"RADAR_ALT_BUG", 2215, "Radar Altimeter bug: Adjust"  # to 10m
"LASING_BUTTON_COVER", 1, "Lasing button cover: Open"
"MISSILE_LAUNCH_COVER", 1, "Missile launch button cover: Open"
"FLARE_DISP_FIRE_CAP", 1, "Flare Dispenser cover: Open"
"WEAPONS_MASTER_ARM", 1, "Master Arm: Marche"
"ANTICOLL_LIGHTS", 1, "Anticollision lights: Arret"
