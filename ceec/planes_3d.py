from manimlib import *

class ceecproblem3DScene(InteractiveScene):
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

        #add plane z=0
        xyspan = 5
        plane1 = ParametricSurface(
            lambda u, v: np.array([u,v, 0]),
            u_range=(-xyspan, xyspan),
            v_range=(-xyspan, xyspan),
            resolution=(30, 30),
            color=YELLOW_E,
            opacity=0.5,
        )
        self.add(plane1)

        #add plane x=0
        xyspan = 5
        plane2 = ParametricSurface(
            lambda u, v: np.array([u,v,0 ]),
            u_range=(-xyspan, xyspan),
            v_range=(-xyspan, xyspan),
            resolution=(30, 30),
            color=BLUE_E,
            opacity=0.5,
        )
        plane2.rotate(90* DEGREES, RIGHT)
        self.add(plane2)

        #add lines, Remember these ways to add a line!
        main_line = Line(ORIGIN, axes_3d.c2p(4,3,xyspan), color=RED)
        verticle_line = DashedLine(axes_3d.c2p(4,0), axes_3d.c2p(4,3))
        horizontal_line = DashedLine(axes_3d.c2p(0,3), axes_3d.c2p(4,3))
        fall_line = DashedLine(axes_3d.c2p(4,3), axes_3d.c2p(4,3, xyspan))
        self.add(main_line, verticle_line, horizontal_line, fall_line)

        #trying out Tex
        t = Text("Hallo Leute")
        t.shift(LEFT_SIDE)
        t.shift(TOP)
        self.add(t)