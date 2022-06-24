import cadquery as cq
from cadquery import exporters
from config import *
from timeit import default_timer as timer


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


def add_horizontal_lines(face):
    '''
    Add the horizontal lines above and below the voltage switches
    and return the modified face.
    '''
    def add_h_lines(face, endpoints, center_y):
        for pts in endpoints:

            center_x = (pts[0] + pts[1])/2
            line_len = abs(pts[0] - pts[1])

            face = (
                face.
                center(center_x, center_y)
                .rect(
                    line_len,
                    LINE_WIDTH
                )
                .cutBlind(ENGRAVE_DEPTH)
                .center(-center_x, -center_y)
            )
        return face

    face = add_h_lines(
        face,
        voltage_label_lines["endpoints"],
        voltage_label_lines["center y"]
    )

    face = add_h_lines(
        face,
        voltage_intensity_lines["endpoints"],
        voltage_intensity_lines["center y"]
    )

    return face


def add_small_vertical_bars(face):
    '''
    Add the small vertical bars at the rightmost ends
    of the horizontal lines and return the modified face
    '''
    def add_v_lines(face, center_y):
        center_x = small_vertical_bars["x coord"]

        line_len = small_vertical_bars["height"]

        face = (
            face.
            center(center_x, center_y)
            .rect(
                LINE_WIDTH,
                line_len,
            )
            .cutBlind(ENGRAVE_DEPTH)
            .center(-center_x, -center_y)
        )
        return face

    face = add_v_lines(
        face,
        voltage_label_lines["center y"]
    )

    face = add_v_lines(
        face,
        voltage_intensity_lines["center y"]
    )
    return face


def cut_vernier_dials(face):
    '''
    Cut the vernier dials and the voltmeter and return the modified face.
    '''
    for _, dial in dials.items():
        coord = dial["coordinate"]
        face = (
            face
            .center(*coord)
            .polarArray(  # the triangular mounting holes
                radius=dial["model"]["mounting hole dist"],
                startAngle=90,
                angle=120,
                count=3,
                fill=False
            )
            .hole(dial["model"]["mounting hole dia"])
            .center(-coord[0], -coord[1])  # recenter the origin
            .workplane()
            .moveTo(*coord)
            .hole(dial["model"]["center hole dia"])  # the center hole
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


# list of all the panel modifying functions
funcs = [
    cut_voltage_lamps,
    add_horizontal_lines,
    add_small_vertical_bars,
    cut_voltage_switches,
    cut_misc_holes,
    cut_vernier_dials,
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
