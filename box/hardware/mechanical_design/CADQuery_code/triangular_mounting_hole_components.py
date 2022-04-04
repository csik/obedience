class Triangular_Mounting_Hole_Component():
    '''
    Generic class for components with a center hole and triangular mounting 
    holes. Add subclasses as needed to create new footprints.
    '''

    def __init__(self, center_hole_diameter, mounting_hole_dist_from_center, mounting_screw_diameter):
        self.mounting_hole_dist_from_center = mounting_hole_dist_from_center
        self.center_hole_diameter = center_hole_diameter
        self.mounting_screw_diameter = mounting_screw_diameter

    def cut(self, panel, coord):
        '''
        Make a cutout for the component in the 
        given panel centered at the (x, y) coordinate.

        Args:
            panel (cadquery.cq.Workplane): the panel to add a component to
            coord (number, number): the (x, y) coordinate of the component center

        Returns:
            the modified panel.
        '''
        panel = (
            panel
            .center(*coord)
            .polarArray(  # the triangular mounting holes
                radius=self.mounting_hole_dist_from_center,
                startAngle=0,
                angle=120,
                count=3,
                fill=False
            )
            .hole(self.mounting_screw_diameter)
            .center(-coord[0], -coord[1])  # recenter the origin
            .workplane()
            .moveTo(*coord)
            .hole(self.center_hole_diameter)  # the center hole
        )

        return panel


class Philmore_S36(Triangular_Mounting_Hole_Component):
    def __init__(self):
        Triangular_Mounting_Hole_Component.__init__(self, 6.3, 20, 3.2)


class Philmore_S50(Triangular_Mounting_Hole_Component):
    def __init__(self):
        Triangular_Mounting_Hole_Component.__init__(self,  6.3, 28, 3.2)


class Voltmeter_62C2(Triangular_Mounting_Hole_Component):
    def __init__(self):
        Triangular_Mounting_Hole_Component.__init__(self,  70, 38, 3.2)
