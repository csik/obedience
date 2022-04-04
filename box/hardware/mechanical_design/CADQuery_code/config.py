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
HEIGHT = 500
THICKNESS = 1
PANEL_SIZE = (LENGTH, HEIGHT, THICKNESS)

X_ORIGIN = 0
Y_ORIGIN = 0

################################################################################
#
# TEXT AND FONT SIZES
#
################################################################################
FONTSIZE_SMALL = 4
FONTSIZE_MEDIUM = 6
FONTSIZE_LARGE = 10

LINE_WIDTH = 1

ENGRAVE_DEPTH = 0.2

################################################################################
#
# VOLTAGE SWITCH AND VOLTAGE INDICATOR LAMPS
#
################################################################################

#######################################
# VOLTAGE SWITCHES
#######################################
NUM_VOLTAGE_SWITCHES = 30

VOLTAGE_SWITCH_X_SPACING = 30

VOLTAGE_SWITCH_CENTER_Y = -75

switch = Mossman_4PDT_Leaf_Switch()

#######################################
# VOLTAGE SWITCH V. LABEL TEXT
#######################################
VOLTAGE_SWITCH_STARTING_VOLTAGE = 15
VOLTAGE_SWITCH_VOLTAGE_STEP = 15
VOLTAGE_LABEL_CENTER_Y = -25

VOLTAGE_LABEL_BIG_TEXT_OFFSET = 3

VOLTAGE_LABEL_SMALL_TEXT_OFFSET = 5

VOLTAGE_LABEL_HORIZ_LINE_LENGTHS = [
    95,
    95,
    95,
    95,
    95,
    95,
    95
]

#######################################
# VOLTAGE SWITCH INTENSITY TEXT
#######################################
LAST_VOLTAGE_INTENSITY_TEXT_POS = 26

VOLTAGE_INTENSITY_TEXT_Y_SPACING = 10

TOP_OF_TWO = 5
BOTTOM_OF_TWO = TOP_OF_TWO - VOLTAGE_INTENSITY_TEXT_Y_SPACING

TOP_OF_THREE = TOP_OF_TWO
MIDDLE_OF_THREE = BOTTOM_OF_TWO
BOTTOM_OF_THREE = MIDDLE_OF_THREE - VOLTAGE_INTENSITY_TEXT_Y_SPACING

VOLTAGE_INTENSITY_HORIZ_LINE_LENGTHS = [
    45,
    45,
    45,
    45,
    45,
    45,
    45
]

voltage_intensity_text = {
    "center y": -150,
    "label": [
        [
            {
                "body": "SLIGHT",
                "y offset": TOP_OF_TWO
            },
            {
                "body": "SHOCK",
                "y offset": BOTTOM_OF_TWO
            }
        ],
        [
            {
                "body": "MODERATE",
                "y offset": TOP_OF_TWO
            },
            {
                "body": "SHOCK",
                "y offset": BOTTOM_OF_TWO
            }
        ],
        [
            {
                "body": "STRONG",
                "y offset": TOP_OF_TWO
            },
            {
                "body": "SHOCK",
                "y offset": BOTTOM_OF_TWO
            }
        ],
        [
            {
                "body": "VERY STRONG",
                "y offset": TOP_OF_TWO
            },
            {
                "body": "SHOCK",
                "y offset": BOTTOM_OF_TWO
            }
        ],
        [
            {
                "body": "INTENSE",
                "y offset": TOP_OF_TWO
            },
            {
                "body": "SHOCK",
                "y offset": BOTTOM_OF_TWO
            }
        ],
        [
            {
                "body": "EXTREME",
                "y offset": TOP_OF_THREE
            },
            {
                "body": "INTENSITY",
                "y offset": MIDDLE_OF_THREE
            },
            {
                "body": "SHOCK",
                "y offset": BOTTOM_OF_THREE
            }
        ],
        [
            {
                "body": "DANGER:",
                "y offset": TOP_OF_TWO
            },
            {
                "body": "SEVERE SHOCK",
                "y offset": BOTTOM_OF_TWO
            }
        ],
    ],
    "fontsize": FONTSIZE_LARGE
}

#######################################
# VOLTAGE LAMPS
#######################################

NUM_VOLTAGE_LAMPS = NUM_VOLTAGE_SWITCHES

VOLTAGE_LAMP_DIAMETER = 16

VOLTAGE_LAMP_CENTER_Y = 0

VOLTAGE_LAMP_NUMS_CENTER_Y = VOLTAGE_LAMP_CENTER_Y + 15

VOLTAGE_LAMP_X_SPACING = VOLTAGE_SWITCH_X_SPACING

VOLTAGE_LAMP_Y_SPACING = 1

VOLTAGE_LAMP_NUM_ROWS = 1


################################################################################
#
# LARGE VERNIER DIALS AND VOLTMETER
#
################################################################################
dials = {
    "attenuator": {
        "model": Philmore_S36(),
        "coordinate": (0, 75),
        "text": [
            {
                "body": "ATTENUATOR",
                "offset": (-50, 0),
                "fontsize": FONTSIZE_MEDIUM
            }
        ]
    },
    "phase dial": {
        "model": Philmore_S50(),
        "coordinate": (150, 100),
        "text": [
            {
                "body": "PHASE",
                "offset": (0, 50),
                "fontsize": FONTSIZE_LARGE
            },
            {
                "body": "PULSE FREQUENCY",
                "offset": (0, -35),
                "fontsize": FONTSIZE_MEDIUM
            }
        ]
    },
    "voltmeter": {
        "model": Voltmeter_62C2(),
        "coordinate": (330, 125),
        "text": [
            {
                "body": "VOLTAGE",
                "offset": (0, -50),
                "fontsize": FONTSIZE_LARGE
            }
        ]
    }
}

################################################################################
#
# MISC. HOLES AND SWITCHES
#
################################################################################
misc_holes = {
    "on off switch": {
        "diameter": 16,
        "coordinate": (-120, 100),
        "text": [
            {
                "body": "MAIN POWER",
                "offset": (0, -15),
                "fontsize": FONTSIZE_MEDIUM
            },
            {
                "body": "ON",
                "offset": (-20, 0),
                "fontsize": FONTSIZE_MEDIUM
            },
            {
                "body": "OFF",
                "offset": (20, 0),
                "fontsize": FONTSIZE_MEDIUM
            }
        ]
    },
    "on off lamp": {
        "diameter": 16,
        "coordinate": (-120, 150),
        "text": []
    },
    "energizer lamp": {
        "diameter": 16,
        "coordinate": (0, 150),
        "text": [
            {
                "body": "VOLTAGE",
                "offset": (-50, 5),
                "fontsize": FONTSIZE_MEDIUM
            },
            {
                "body": "ENERGIZER",
                "offset": (-50, -5),
                "fontsize": FONTSIZE_MEDIUM
            }
        ]
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
