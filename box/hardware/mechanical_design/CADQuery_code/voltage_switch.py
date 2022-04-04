class Voltage_Switch():
    '''
    Generic voltage switch class. Add subclasses as needed to change the 
    voltage switch footprints.
    '''

    def cut(self, panel, coord):
        '''
          Make a cutout for the switch in the 
          given panel centered at the (x, y) coordinate.

          Args:
              panel (cadquery.cq.Workplane): the panel to add a switch to
              coord (number, number): the (x, y) coordinate of the switch center

          Returns:
              the modified panel.
          '''
        return panel


class Mossman_4PDT_Leaf_Switch(Voltage_Switch):
    '''
    Mossman style leaf switch. 4PDT. 5 amp. Maintained - OFF - Momentary
    (SWZ) CDM-24143, found here:
    https://www.surplussales.com/Switches/SWLeaf-1.html
    '''

    # TODO: these dimensions are just rough guesses.
    # carefully measure the real switch and enter
    # the correct dimensions before production
    SLOT_LENGTH = 35
    SLOT_WIDTH = 5

    MOUNTING_HOLE_X_SPACING = 16
    MOUNTING_HOLE_Y_SPACING = 32

    MOUNTING_HOLE_DIA = 2

    PERPENDICULAR = 90

    def cut(self, panel, coord):
        # cut the slot
        panel = (
            panel
            .moveTo(*coord)
            .slot2D(self.SLOT_LENGTH, self.SLOT_WIDTH, self.PERPENDICULAR)
            .cutThruAll()
        )

        # cut the four mounting holes
        panel = (
            panel
            .moveTo(*coord)
            .rect(
                self.MOUNTING_HOLE_X_SPACING,
                self.MOUNTING_HOLE_Y_SPACING,
                forConstruction=True
            )
            .vertices()
            .hole(self.MOUNTING_HOLE_DIA)
        )
        return panel
