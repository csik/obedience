from voltage_switch import Mossman_4PDT_Leaf_Switch
from triangular_mounting_hole_components import Philmore_S36, Philmore_S50, Voltmeter_62C2
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
# LARGE VERNIER DIALS
#
################################################################################
attenuator_dial = Philmore_S36()
ATTENUATOR_DIAL_COORD = (0, 50)

phase_dial = Philmore_S50()
PHASE_DIAL_COORD = (150, 75)

################################################################################
#
# ANALOG VOLTMETER
#
################################################################################
voltmeter = Voltmeter_62C2()
VOLTMETER_COORD = (330, 75)

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
    "energizer lamp": {
        "diameter": 16,
        "coordinates": (0, 100)
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
