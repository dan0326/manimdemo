from manimlib import *
from manimlib.utils import color

class My3DScene(InteractiveScene):
    def construct(self):
        # Set up the 3D axes
        axes_3d = ThreeDAxes(
            z_range=(-3, 3, 1),
            depth=6
        )
        axes_3d.set_width(FRAME_WIDTH)
        axes_3d.center()
        self.frame.reorient(43, 76, 1, IN, 10)
        self.add(axes_3d)

        #add lines, Remember these ways to add a line!
        main_line = Line(ORIGIN, axes_3d.c2p(4,3,2), color=RED)
        verticle_line = DashedLine(axes_3d.c2p(4,0), axes_3d.c2p(4,3))
        horizontal_line = DashedLine(axes_3d.c2p(0,3), axes_3d.c2p(4,3))
        fall_line = DashedLine(axes_3d.c2p(4,3), axes_3d.c2p(4,3, 2))
        self.add(main_line, verticle_line, horizontal_line, fall_line)

        #trying out Tex
        t = Text("Hallo Leute")
        t.move_to(TOP)
        self.add(t)


