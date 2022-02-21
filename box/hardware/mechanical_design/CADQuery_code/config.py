from voltage_switch import Mossman_4PDT_Leaf_Switch
import os

# TODO: All dimensions are rough guesses. Once we have accurate dimensions,
# they will need to be entered in the various fields in this file


################################################################################
#
# PANEL DIMENSIONS
#
################################################################################
LENGTH = 1000
HEIGHT = 300
THICKNESS = 1
PANEL_SIZE = (LENGTH, HEIGHT, THICKNESS)

X_ORIGIN = 0
Y_ORIGIN = 0


################################################################################
#
# VOLTAGE SWITCH AND VOLTAGE INDICATOR LAMPS
#
################################################################################
NUM_VOLTAGE_SWITCHES = 30

VOLTAGE_SWITCH_X_SPACING = 30

VOLTAGE_SWITCH_TOTAL_X_SPACING = (NUM_VOLTAGE_SWITCHES - 1) * \
    VOLTAGE_SWITCH_X_SPACING

VOLTAGE_SWITCH_CENTER_Y = -50

NUM_VOLTAGE_LAMPS = NUM_VOLTAGE_SWITCHES

VOLTAGE_LAMP_DIAMETER = 16

VOLTAGE_LAMP_CENTER_Y = 0

VOLTAGE_LAMP_X_SPACING = VOLTAGE_SWITCH_X_SPACING

VOLTAGE_LAMP_Y_SPACING = 1

VOLTAGE_LAMP_NUM_ROWS = 1

switch = Mossman_4PDT_Leaf_Switch()


################################################################################
#
# MISC. DIALS AND SWITCHES
#
################################################################################
misc_holes = {
    "on off switch": {
        "diameter": 16,
        "coordinates": (-120, 60)
    },
    "on off lamp": {
        "diameter": 16,
        "coordinates": (-120, 100)
    },
    "attenuator knob": {
        "diameter": 30,
        "coordinates": (0, 50)
    },
    "energizer lamp": {
        "diameter": 16,
        "coordinates": (0, 100)
    },
    "phase knob": {
        "diameter": 50,
        "coordinates": (150, 75)
    },
    "voltage meter": {
        "diameter": 70,
        "coordinates": (330, 75)
    }
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
    os.path.join(OUTPUT_FILE_DIR, "out.step")
]
