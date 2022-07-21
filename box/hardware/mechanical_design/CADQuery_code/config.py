
import os

# TODO: Double check the panel and tweak as needed

# ALL DIMENSIONS ARE IN UNITS OF MILLIMETERS
# ALL POSITIONS ARE RELATIVE TO THE CENTER OF THE PANEL

################################################################################
#
# PANEL DIMENSIONS
#
################################################################################
PANEL_LENGTH = 914.4
PANEL_HEIGHT = 406.4
PANEL_THICKNESS = 1
PANEL_SIZE = (PANEL_LENGTH, PANEL_HEIGHT, PANEL_THICKNESS)

X_ORIGIN = 0
Y_ORIGIN = 0

# a few common hole sizes that show up a lot
LAMP_HOLE_DIA = 14.2
TOGGLE_SWITCH_HOLE_DIA = 12
M3_HOLE_DIA = 3.2

################################################################################
#
# VOLTAGE SWITCH AND VOLTAGE INDICATOR LAMPS
#
################################################################################

#######################################
# VOLTAGE SWITCHES
#######################################
voltage_switch = {
    "num switches": 30,
    "num rows": 1,
    "x spacing": 25.4,
    "y spacing": 1,
    "center y": -60.5,
    "slot length": 19.05,
    "slot width": 4.7625,
    "perpendicular": 90,
}


#######################################
# VOLTAGE LAMPS
#######################################

voltage_lamp = {
    "num lamps": voltage_switch["num switches"],
    "num rows": voltage_switch["num rows"],
    "x spacing": voltage_switch["x spacing"],
    "y spacing": voltage_switch["y spacing"],
    "lamp center y": 0,
    "nums center y": 25,
    "diameter": LAMP_HOLE_DIA,
}

################################################################################
#
# LARGE VERNIER DIALS AND VOLTMETER
#
################################################################################

philmore_S36 = {
    "center hole dia": 10.5,
    "dist to top hole": 19.5,
    "dist to bottom holes": 22,
    "bottom hole angle": 45,
    "mounting hole dia": M3_HOLE_DIA
}

philmore_S50 = {
    "center hole dia": 10.5,
    "dist to top hole": 27.5,
    "dist to bottom holes": 30,
    "bottom hole angle": 45,
    "mounting hole dia": M3_HOLE_DIA
}

seiki_N301 = {
    "center hole dia": 10.5,
    "dist to top hole": 37.5,
    "dist to bottom holes": 40,
    "bottom hole angle": 45,
    "mounting hole dia": M3_HOLE_DIA
}

dials = {
    "attenuator": {
        "model": philmore_S36,
        "coordinate": (25.4, 65),
    },
    "phase dial": {
        "model": seiki_N301,
        "coordinate": (147, 90),
    }
}

voltmeter_62C2 = {
    "coordinate": (304.5, 106),
    "center hole dia": 70,
    "mounting hole dist": 39.26,
    "mounting hole dia": M3_HOLE_DIA
}

voltmeter = voltmeter_62C2

################################################################################
#
# MISC. HOLES, LAMPS, AND SWITCHES
#
################################################################################
misc_holes = {
    "on off switch": {
        "diameter": TOGGLE_SWITCH_HOLE_DIA,
        "coordinate": (-114.5, 87.5),
    },
    "on off lamp": {
        "diameter": LAMP_HOLE_DIA,
        "coordinate": (-114.5, 127.5),
        "text": []
    },
    "energizer lamp": {
        "diameter": LAMP_HOLE_DIA,
        "coordinate": (21.5, 127.5),
    }
}

WOOD_SCREW_HOLES_DIA = M3_HOLE_DIA

# the main woodscrew holes seem to be vertically symmetric about the center of the voltage switches
WOOD_SCREW_HOLES_VERT_DIST_FROM_SWITCHES = 25
WOOD_SCREW_HOLES_TOP_ROW_CENTER_Y = voltage_switch["center y"] + \
    WOOD_SCREW_HOLES_VERT_DIST_FROM_SWITCHES
WOOD_SCREW_HOLES_BOTTOM_ROW_CENTER_Y = voltage_switch["center y"] - \
    WOOD_SCREW_HOLES_VERT_DIST_FROM_SWITCHES

# they seem to be symmetric about the center line too
WOOD_SCREW_HOLES_RIGHTMOST_CENTER_X = 390
WOOD_SCREW_HOLES_MIDDLE_RIGHT_CENTER_X = 100
WOOD_SCREW_HOLES_LEFTMOST_CENTER_X = -WOOD_SCREW_HOLES_RIGHTMOST_CENTER_X
WOOD_SCREW_HOLES_MIDDLE_LEFT_CENTER_X = -WOOD_SCREW_HOLES_MIDDLE_RIGHT_CENTER_X

# there are a handful of woodscrews that don't fit the pattern, these may have been hand drilled
# after the original panel was machined or something

wood_screw_holes = [
    # leftmost 4 holes
    {
        "diameter": WOOD_SCREW_HOLES_DIA,
        "coordinate": (WOOD_SCREW_HOLES_LEFTMOST_CENTER_X, -17.5)
    },
    {
        "diameter": WOOD_SCREW_HOLES_DIA,
        "coordinate": (WOOD_SCREW_HOLES_LEFTMOST_CENTER_X, WOOD_SCREW_HOLES_TOP_ROW_CENTER_Y)
    },
    {
        "diameter": WOOD_SCREW_HOLES_DIA,
        "coordinate": (WOOD_SCREW_HOLES_LEFTMOST_CENTER_X, WOOD_SCREW_HOLES_BOTTOM_ROW_CENTER_Y)
    },
    {
        "diameter": WOOD_SCREW_HOLES_DIA,
        "coordinate": (-365, WOOD_SCREW_HOLES_TOP_ROW_CENTER_Y)
    },
    # middle left 2 holes
    {
        "diameter": WOOD_SCREW_HOLES_DIA,
        "coordinate": (WOOD_SCREW_HOLES_MIDDLE_LEFT_CENTER_X, WOOD_SCREW_HOLES_TOP_ROW_CENTER_Y)
    },
    {
        "diameter": WOOD_SCREW_HOLES_DIA,
        "coordinate": (WOOD_SCREW_HOLES_MIDDLE_LEFT_CENTER_X, WOOD_SCREW_HOLES_BOTTOM_ROW_CENTER_Y)
    },
    # middle right 2 holes
    {
        "diameter": WOOD_SCREW_HOLES_DIA,
        "coordinate": (WOOD_SCREW_HOLES_MIDDLE_RIGHT_CENTER_X, WOOD_SCREW_HOLES_TOP_ROW_CENTER_Y)
    },
    {
        "diameter": WOOD_SCREW_HOLES_DIA,
        "coordinate": (WOOD_SCREW_HOLES_MIDDLE_RIGHT_CENTER_X, WOOD_SCREW_HOLES_BOTTOM_ROW_CENTER_Y)
    },
    # rightmost 2 holes
    {
        "diameter": WOOD_SCREW_HOLES_DIA,
        "coordinate": (WOOD_SCREW_HOLES_RIGHTMOST_CENTER_X, -23.5)
    },
    {
        "diameter": WOOD_SCREW_HOLES_DIA,
        "coordinate": (WOOD_SCREW_HOLES_RIGHTMOST_CENTER_X, WOOD_SCREW_HOLES_BOTTOM_ROW_CENTER_Y)
    },
]

################################################################################
#
# MOUNTING HOLES AROUND THE OUTER EDGE (not present in original, but might be handy)
#
################################################################################

mounting_holes = {
    "dist from edge": 6.35,
    "hole dia": M3_HOLE_DIA,
    "num horizontal": 3,
    "num vertical": 1
}


################################################################################
#
# OUTPUT FILES
#
################################################################################
OUTPUT_FILE_DIR = os.path.join("..", "out")

os.makedirs(OUTPUT_FILE_DIR, exist_ok=True)

output_files = [
    os.path.join(OUTPUT_FILE_DIR, "out.stl"),
    os.path.join(OUTPUT_FILE_DIR, "out.step"),
    os.path.join(OUTPUT_FILE_DIR, "out.dxf"),
    os.path.join(OUTPUT_FILE_DIR, "out.svg"),
]
