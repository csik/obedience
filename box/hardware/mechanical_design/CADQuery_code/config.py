
import os

# TODO: Double check the panel and tweak as needed
# The verier dials and voltmeter almost certanly need tweaks.

# ALL DIMENSIONS ARE IN UNITS OF MILLIMETERS
# ALL POSITIONS ARE RELATIVE TO THE CENTER OF THE PANEL

################################################################################
#
# PANEL DIMENSIONS
#
################################################################################
LENGTH = 914.4
HEIGHT = 406.4
THICKNESS = 1
PANEL_SIZE = (LENGTH, HEIGHT, THICKNESS)

X_ORIGIN = 0
Y_ORIGIN = 0

LINE_WIDTH = 1
ENGRAVE_DEPTH = -0.5

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
    "starting voltage": 15,
    "voltage step": 15
}

#######################################
# VOLTAGE SWITCH V. LABEL LINES
#######################################

voltage_label_lines = {
    "center y": -23.5,
    "endpoints": [
        (-364.9, -280.5),
        (-262.0, -178.5),
        (-159.7, -74.5),
        (-56.6, 27.0),
        (45.0, 128.5),
        (146.3, 229.4),
        (247.9, 327.5),
    ]
}

#######################################
# VOLTAGE SWITCH INTENSITY LINES
#######################################

voltage_intensity_lines = {
    "center y": -106,
    "endpoints": [
        (-356.4, -292.0),
        (-247.6, -184.4),
        (-151.7, -94.8),
        (-38.4, 17.5),
        (53.1, 116.8),
        (159.2, 209),
        (262.2, 327.5)
    ]
}

#######################################
# SMALL VERTICAL BARS
#######################################

small_vertical_bars = {
    "height": 10.5,
    "x coord": 327.5,
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
    "diameter": 12.7,
}

################################################################################
#
# LARGE VERNIER DIALS AND VOLTMETER
#
################################################################################

philmore_S36 = {
    "center hole dia": 6.3,
    "mounting hole dist": 20,
    "mounting hole dia": 3.2
}

philmore_S50 = {
    "center hole dia": 6.3,
    "mounting hole dist": 28,
    "mounting hole dia": 3.2
}

voltmeter_62C2 = {
    "center hole dia": 70,
    "mounting hole dist": 38,
    "mounting hole dia": 3.2
}

dials = {
    "attenuator": {
        "model": philmore_S36,
        "coordinate": (23, 65),
    },
    "phase dial": {
        "model": philmore_S50,
        "coordinate": (147, 95),
    },
    "voltmeter": {
        "model": voltmeter_62C2,
        "coordinate": (304.5, 106),
    }
}

################################################################################
#
# MISC. HOLES, LAMPS, AND SWITCHES
#
################################################################################
misc_holes = {
    "on off switch": {
        "diameter": 12.7,
        "coordinate": (-117.5, 87.5),
    },
    "on off lamp": {
        "diameter": 12.7,
        "coordinate": (-117.5, 127.5),
        "text": []
    },
    "energizer lamp": {
        "diameter": 12.7,
        "coordinate": (20.6, 127.5),
    }
}

wood_screw_holes = [
    # leftmost 4 holes
    {
        "diameter": 3,
        "coordinate": (-395, -17.5)
    },
    {
        "diameter": 3,
        "coordinate": (-395, -33)
    },
    {
        "diameter": 3,
        "coordinate": (-395, -80)
    },
    {
        "diameter": 3,
        "coordinate": (-370, -33)
    },
    # middle left 2 holes
    {
        "diameter": 3,
        "coordinate": (-104, -33)
    },
    {
        "diameter": 3,
        "coordinate": (-104, -80)
    },
    # middle right 2 holes
    {
        "diameter": 3,
        "coordinate": (99, -33)
    },
    {
        "diameter": 3,
        "coordinate": (99, -80)
    },
    # rightmost 2 holes
    {
        "diameter": 3,
        "coordinate": (383, -23.5)
    },
    {
        "diameter": 3,
        "coordinate": (383, -80)
    },
]

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
