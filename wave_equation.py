from manimlib import *

#funcions to get the curve on complex plain
def get_complex_graph(axes, func, delta_x=0.01):

    x_min, x_max, _ = axes.x_axis.x_range

    xs = np.arange(x_min, x_max, delta_x)
    zs=func(xs)
    points=np.array([
        (x, psi.real, psi.imag)
        for x ,psi in zip(xs, zs)
    ])
    curve = VMobject()
    curve.set_points_smoothly(axes.c2p(*points.T))
    return curve

class SchrodingerPlay(InteractiveScene):
    def construct(self):
        #axes
        x_max=3
        axes= ThreeDAxes(
            x_range=(0, 10),
            y_range=(-x_max, x_max),
            z_range=(-x_max, x_max)
        )
        self.add(axes)

        #add complex plane
        planes=VGroup()
        for x in range(1, 10):
            plane = ComplexPlane(
                (-x_max, x_max), (-x_max, x_max),
                background_line_style=dict(stroke_color=BLUE, stroke_width=1, stroke_opacity=1),
                faded_line_style=dict(stroke_color=BLUE,stroke_width=1, stroke_opacity=0.5)
            )
            plane.rotate(90 * DEGREES, RIGHT)
            plane.rotate(90 * DEGREES, OUT)
            plane.move_to(axes.c2p(x, 0, 0))
            planes.add(plane)
        plane= planes[2]
        self.add(plane)

        #show one solution
        A=1
        k=1
        w=1
        t=0
        def plane_wave(x):
            return A * np.exp(1j *(k*x-w*t))
        graph= get_complex_graph(axes, plane_wave)
        self.add(graph)

        #add vector and glow dot on a plane
        z_dot = GlowDot()
        z_vect=Vector()
        x = axes.x_axis.p2n(plane.get_center())
        z_dot.move_to(plane.n2p(plane_wave(x)))
        z_vect.put_start_and_end_on(
            plane.n2p(0),
            plane.n2p(plane_wave(x))
        )
        z_vect.rotate(TAU/4, axis=z_vect.get_vector())
        z_vect.set_color(YELLOW)
        self.add(z_dot)
        self.add(z_vect)

