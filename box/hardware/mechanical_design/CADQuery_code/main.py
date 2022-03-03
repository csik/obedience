import cadquery as cq
from cadquery import exporters
from config import *


panel = (
    cq.Workplane("XY").box(*PANEL_SIZE)
)

# cut the voltage switches
offset = ((NUM_VOLTAGE_SWITCHES - 1) * VOLTAGE_SWITCH_X_SPACING) / 2.0

for i in range(NUM_VOLTAGE_SWITCHES):
    center_x = i * VOLTAGE_SWITCH_X_SPACING - offset

    panel = switch.cut(
        panel,
        (center_x, VOLTAGE_SWITCH_CENTER_Y)
    )

# cut the voltage indicator lamps
panel = (
    panel
    .faces(">Z")
    .workplane()
    .center(X_ORIGIN, VOLTAGE_LAMP_CENTER_Y)
    .rarray(
        VOLTAGE_LAMP_X_SPACING,
        VOLTAGE_LAMP_Y_SPACING,
        NUM_VOLTAGE_LAMPS,
        VOLTAGE_LAMP_NUM_ROWS
    )
    .hole(VOLTAGE_LAMP_DIAMETER)
)

# cut the vernier dials
panel = (
    attenuator_dial.cut(
        panel,
        ATTENUATOR_DIAL_COORD
    )
)

panel = (
    phase_dial.cut(
        panel,
        PHASE_DIAL_COORD
    )
)

# cut the voltmeter
panel = (
    voltmeter.cut(
        panel,
        VOLTMETER_COORD
    )
)

# cut the misc. holes
for _, v in misc_holes.items():
    panel = (
        panel.
        faces(">Z")
        .workplane()
        .moveTo(*v["coordinates"])
        .hole(v["diameter"])
    )

# export outputs
for output in output_files:
    exporters.export(panel, output)
