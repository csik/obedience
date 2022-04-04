import cadquery as cq
from cadquery import exporters
from config import *
from timeit import default_timer as timer


panel = (
    cq.Workplane("XY").box(*PANEL_SIZE)
)

face = panel.faces(">Z").workplane()

VOLTAGE_SWITCH_X_OFFSET = ((NUM_VOLTAGE_SWITCHES - 1)
                           * VOLTAGE_SWITCH_X_SPACING) / 2.0


def add_text(face, coord, text, fontsize=FONTSIZE_MEDIUM, fontPath=None, halign='center', valign='center'):
    '''
    Add generic text to the given face and return the modified face
    '''
    face = (
        face
        .center(coord[0], coord[1])
        .text(
            text,
            fontsize=fontsize,
            distance=-ENGRAVE_DEPTH,
            combine='cut',
            fontPath=fontPath,
            halign=halign,
            valign=valign
        )
        .center(-coord[0], -coord[1])
    )
    return face


def add_warning_text(face):
    '''
    Add some warning text to make it clear that the panel is not
    ready to be ordered yet.
    '''
    face = add_text(
        face,
        (-350, 200),
        "WARNING: WIP",
        24
    )
    face = add_text(
        face,
        (-350, 180),
        "Not ready to order",
        18
    )

    return face


def cut_voltage_switches(face):
    '''
    Cut the voltage switches in the given face and return the modified face
    '''
    for i in range(NUM_VOLTAGE_SWITCHES):
        center_x = i * VOLTAGE_SWITCH_X_SPACING - VOLTAGE_SWITCH_X_OFFSET

        face = switch.cut(
            face,
            (center_x, VOLTAGE_SWITCH_CENTER_Y)
        )
    return face


def cut_voltage_lamps(face):
    '''
    Cut the voltage lamps in the given face and return the modified face.
    These are the 30 round numbered lamps above the voltage switches. 
    '''
    for i in range(NUM_VOLTAGE_SWITCHES):
        center_x = i * VOLTAGE_SWITCH_X_SPACING - VOLTAGE_SWITCH_X_OFFSET

        face = (
            face
            .moveTo(center_x, VOLTAGE_LAMP_CENTER_Y)
            .hole(VOLTAGE_LAMP_DIAMETER)
        )
    return face


def add_voltage_lamp_nums(face):
    '''
    Add the labels 1..30 above the voltage lamps.
    '''
    for i in range(NUM_VOLTAGE_SWITCHES):
        center_x = i * VOLTAGE_SWITCH_X_SPACING - VOLTAGE_SWITCH_X_OFFSET

        face = add_text(
            face,
            (
                center_x,
                VOLTAGE_LAMP_NUMS_CENTER_Y
            ),
            str(i + 1)
        )
    return face


def add_voltage_intensity_text(face):
    '''
    Add the shock intensity text below the voltage switches. Starting with 
    "SLIGHT SHOCK" below the first switch, skipping 3 switches, then 
    "MODERATE SHOCK" below the 5th switch, etc
    '''
    for i in range(NUM_VOLTAGE_SWITCHES):
        center_x = i * VOLTAGE_SWITCH_X_SPACING - VOLTAGE_SWITCH_X_OFFSET

        # start at the 1st switch and do every 4th switch
        if i % 4 == 0 and i < LAST_VOLTAGE_INTENSITY_TEXT_POS:
            for txt in voltage_intensity_text["label"][i // 4]:
                face = add_text(
                    face,
                    (
                        center_x,
                        voltage_intensity_text["center y"] + txt["y offset"]
                    ),
                    txt["body"],
                    voltage_intensity_text["fontsize"]
                )

    # there is an "X X X" at the high-voltage end of the intensity text
    start_of_triple_X = (NUM_VOLTAGE_SWITCHES - 2) * \
        VOLTAGE_SWITCH_X_SPACING - VOLTAGE_SWITCH_X_OFFSET

    face = add_text(
        face,
        (
            start_of_triple_X,
            voltage_intensity_text["center y"]
        ),
        "X  X  X",
        voltage_intensity_text["fontsize"]
    )
    return face


def add_big_voltage_labels(face):
    '''
    Add the big voltage labels between the voltage switches and the lamps,
    "15 volts", [skip 3 switches], "75 vots", [skip 3 switches], "135 VOLTS", etc.
    The last two switches don't follow the normal patter, they are also added here.
    '''
    for i in range(NUM_VOLTAGE_SWITCHES):
        center_x = i * VOLTAGE_SWITCH_X_SPACING - VOLTAGE_SWITCH_X_OFFSET

        # start at the 1st switch and do every 4th switch
        if i % 4 == 0 and i < LAST_VOLTAGE_INTENSITY_TEXT_POS:
            face = add_text(
                face,
                (
                    center_x,
                    VOLTAGE_LABEL_CENTER_Y + VOLTAGE_LABEL_BIG_TEXT_OFFSET,
                    FONTSIZE_MEDIUM
                ),
                str((i + 1) * VOLTAGE_SWITCH_STARTING_VOLTAGE)
            )
            face = add_text(
                face,
                (
                    center_x,
                    VOLTAGE_LABEL_CENTER_Y - VOLTAGE_LABEL_BIG_TEXT_OFFSET,
                    FONTSIZE_MEDIUM
                ),
                "VOLTS"
            )
        # the last two switches have a different pattern, big voltage lettering here,
        # "435 VOLTS" and "450 VOLTS"
        elif i >= NUM_VOLTAGE_SWITCHES - 2:
            face = add_text(
                face,
                (
                    center_x,
                    VOLTAGE_LABEL_CENTER_Y + VOLTAGE_LABEL_BIG_TEXT_OFFSET,
                    FONTSIZE_MEDIUM
                ),
                str((i + 1) * VOLTAGE_SWITCH_STARTING_VOLTAGE)
            )
            face = add_text(
                face,
                (
                    center_x,
                    VOLTAGE_LABEL_CENTER_Y - VOLTAGE_LABEL_BIG_TEXT_OFFSET,
                    FONTSIZE_MEDIUM
                ),
                "VOLTS"
            )
    return face


def add_small_voltage_labels(face):
    '''
    Add the small voltage labels between the voltage switches and the lamps,
    [skip the 1st switch], "30 V.", "45 V.", "60 V.", [skip the 5th switch], etc
    '''
    for i in range(NUM_VOLTAGE_SWITCHES):
        center_x = i * VOLTAGE_SWITCH_X_SPACING - VOLTAGE_SWITCH_X_OFFSET

        if i % 4 == 0 or i >= NUM_VOLTAGE_SWITCHES - 2:
            pass  # this is where the bigger labels go
        else:
            face = add_text(
                face,
                (
                    center_x,
                    VOLTAGE_LABEL_CENTER_Y - VOLTAGE_LABEL_SMALL_TEXT_OFFSET,
                    FONTSIZE_SMALL
                ),
                str((i + 1) * VOLTAGE_SWITCH_STARTING_VOLTAGE) + " V."
            )
    return face


def add_horizontal_lines_above_switches(face):
    '''
    Add the horizontal lines above the voltage switches.
    '''
    for i in range(NUM_VOLTAGE_SWITCHES):
        center_x = i * VOLTAGE_SWITCH_X_SPACING - VOLTAGE_SWITCH_X_OFFSET

        # start at the 3rd switch and do every 4th switch
        if (i + 2) % 4 == 0:
            face = (
                face
                .center(center_x, VOLTAGE_LABEL_CENTER_Y)
                .rect(
                    VOLTAGE_LABEL_HORIZ_LINE_LENGTHS[(i + 1) // 4],
                    LINE_WIDTH
                )
                .cutBlind(-ENGRAVE_DEPTH)
                .center(-center_x, -VOLTAGE_LABEL_CENTER_Y)
            )
    return face


def add_horizontal_lines_below_switches(face):
    '''
    Add the horizontal lines below the voltage switches.
    '''
    for i in range(NUM_VOLTAGE_SWITCHES):
        center_x = i * VOLTAGE_SWITCH_X_SPACING - VOLTAGE_SWITCH_X_OFFSET

        if (i + 2) % 4 == 0:
            face = (
                face
                .center(center_x, voltage_intensity_text["center y"])
                .rect(
                    VOLTAGE_INTENSITY_HORIZ_LINE_LENGTHS[(i + 1) // 4],
                    LINE_WIDTH
                )
                .cutBlind(-ENGRAVE_DEPTH)
                .center(-center_x, -voltage_intensity_text["center y"])
            )
    return face


def add_horizontal_lines(face):
    '''
    Add the horizontal lines above and below the voltage switches.
    '''
    face = add_horizontal_lines_above_switches(face)
    face = add_horizontal_lines_below_switches(face)
    return face


def cut_vernier_dials(face):
    '''
    Cut the vernier dials and the voltmater.
    '''
    for _, dial in dials.items():
        face = (
            dial["model"].cut(
                face,
                dial["coordinate"]
            )
        )

        for txt in dial["text"]:
            face = add_text(
                face,
                (
                    dial["coordinate"][0] + txt["offset"][0],
                    dial["coordinate"][1] + txt["offset"][1],
                ),
                txt["body"],
                txt["fontsize"]
            )
    return face


def cut_misc_holes(face):
    '''
    Cut the various holes, power switch, misc lamps, and misc holes
    '''
    for _, hole in misc_holes.items():
        face = (
            face
            .moveTo(*hole["coordinate"])
            .hole(hole["diameter"])
        )

        for txt in hole["text"]:
            face = add_text(
                face,
                (
                    hole["coordinate"][0] + txt["offset"][0],
                    hole["coordinate"][1] + txt["offset"][1],
                ),
                txt["body"],
                txt["fontsize"]
            )
    return face


# list of all the panel modifying functions
funcs = [
    add_warning_text,
    cut_voltage_switches,
    cut_voltage_lamps,
    add_voltage_lamp_nums,
    add_voltage_intensity_text,
    add_big_voltage_labels,
    add_small_voltage_labels,
    add_horizontal_lines,
    cut_vernier_dials,
    cut_misc_holes
]

# store the times spent on each operation in a dict
func_times = {}

# modify the panel and time each operation
for func in funcs:
    start = timer()
    face = func(face)
    end = timer()
    func_times[func.__name__] = end - start

# turn the 2d face into a 3d panel
start = timer()
panel = face.intersect(panel)
end = timer()
func_times["intersect face and panel"] = end - start

# export outputs
start = timer()
for output in output_files:
    exporters.export(panel, output)
end = timer()
func_times["export stl and step"] = end - start

# print out a summary of the time spent
print("\nTime spent doing each task (seconds):\n")
for k, v in func_times.items():
    print(f"{(k.replace('_', ' ')): <30}{v:.3f}")

print(f"\n{'Total time spent': <30}{sum(func_times.values()):.3f}\n")
