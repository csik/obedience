import cadquery as cq
from cadquery import exporters
from config import *
from timeit import default_timer as timer
import math

panel = (
    cq.Workplane("XY").box(*PANEL_SIZE)
)

face = panel.faces(">Z").workplane()

VOLTAGE_SWITCH_X_OFFSET = ((voltage_switch["num switches"] - 1)
                           * voltage_switch["x spacing"]) / 2.0


def cut_voltage_switches(face):
    '''
    Cut the voltage switches in the given face and return the modified face
    '''
    face = (
        face
        .center(X_ORIGIN, voltage_switch["center y"])
        .rarray(
            voltage_switch["x spacing"],
            voltage_switch["y spacing"],
            voltage_switch["num switches"],
            voltage_switch["num rows"]
        )
        .slot2D(
            voltage_switch["slot length"],
            voltage_switch["slot width"],
            voltage_switch["perpendicular"]
        )
        .cutThruAll()
        .center(-X_ORIGIN, -voltage_switch["center y"])
    )
    return face


def cut_voltage_lamps(face):
    '''
    Cut the voltage lamps in the given face and return the modified face.
    These are the 30 round numbered lamps above the voltage switches.
    '''
    face = (
        face
        .center(X_ORIGIN, voltage_lamp["lamp center y"])
        .rarray(
            voltage_lamp["x spacing"],
            voltage_lamp["y spacing"],
            voltage_lamp["num lamps"],
            voltage_lamp["num rows"]
        )
        .hole(voltage_lamp["diameter"])
        .center(-X_ORIGIN, -voltage_lamp["lamp center y"])
    )
    return face


def cut_vernier_dials(face):
    '''
    Cut the vernier dials and return the modified face.
    '''
    for _, dial in dials.items():
        coord = dial["coordinate"]
        model = dial["model"]
        face = (
            face
            # the center hole
            .moveTo(*coord)
            .hole(model["center hole dia"])

            # the M3 hole at the top
            .moveTo(coord[0], coord[1] + model["dist to top hole"])
            .hole(model["mounting hole dia"])

            # the two M3 holes on the bottom
            .moveTo(
                coord[0] + \
                math.sin(model["bottom hole angle"]) * \
                model["dist to bottom holes"],
                coord[1] - \
                math.cos(model["bottom hole angle"]) * \
                model["dist to bottom holes"]
            )
            .hole(model["mounting hole dia"])

            .moveTo(
                coord[0] - \
                math.sin(model["bottom hole angle"]) * \
                model["dist to bottom holes"],
                coord[1] - \
                math.cos(model["bottom hole angle"]) * \
                model["dist to bottom holes"]
            )
            .hole(model["mounting hole dia"])
        )
    return face


def cut_voltmeter(face):
    '''
    Cut the voltmeter and return the modified face.
    '''
    coord = voltmeter["coordinate"]

    face = (
        face
        .center(*coord)
        # the triangular mounting holes
        .polarArray(
            radius=voltmeter["mounting hole dist"],
            startAngle=90,
            angle=120,
            count=3,
            fill=False
        )
        .hole(voltmeter["mounting hole dia"])
        # recenter the origin
        .center(-coord[0], -coord[1])
        # the big center hole
        .moveTo(*coord)
        .hole(voltmeter["center hole dia"])
    )
    return face


def cut_misc_holes(face):
    '''
    Cut the various holes, power switch, misc lamps, and misc holes
    and return the modified face.
    '''
    for _, hole in misc_holes.items():
        face = (
            face
            .moveTo(*hole["coordinate"])
            .hole(hole["diameter"])
        )

    for hole in wood_screw_holes:
        face = (
            face
            .moveTo(*hole["coordinate"])
            .hole(hole["diameter"])
        )
    return face


def cut_mounting_holes(face):
    '''
    Cut some mounting holes around the perimeter of the panel.
    '''
    x_spacing_top_and_bottom = (PANEL_LENGTH - mounting_holes["dist from edge"]
                                * 2) / (mounting_holes["num horizontal"] - 1)

    y_spacing_top_and_bottom = PANEL_HEIGHT - \
        mounting_holes["dist from edge"]*2

    x_spacing_middle = PANEL_LENGTH - mounting_holes["dist from edge"] * 2

    face = (
        face
        # one row on top and one on the bottom
        .rarray(
            x_spacing_top_and_bottom,
            y_spacing_top_and_bottom,
            mounting_holes["num horizontal"],
            2
        )
        .hole(mounting_holes["hole dia"])
        # two holes centered vertically on the far left and right
        .rarray(
            x_spacing_middle,
            1,  # y-spacing = 1 when there is only one row
            2,  # two total holes
            1  # one row
        )
        .hole(mounting_holes["hole dia"])
    )
    return face


# list of all the panel modifying functions
funcs = [
    cut_voltage_lamps,
    cut_voltage_switches,
    cut_misc_holes,
    cut_vernier_dials,
    cut_voltmeter,
    cut_mounting_holes
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
func_times["export output files"] = end - start

# print out a summary of the time spent
print("\nTime spent doing each task (seconds):\n")
for k, v in func_times.items():
    print(f"{(k.replace('_', ' ')): <30}{v:.3f}")

print(f"\n{'Total time spent': <30}{sum(func_times.values()):.3f}\n")
