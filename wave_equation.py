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
        self.add(planes[2])

        #show one solution
        A=1
        k=1
        w=1
        t=2
        graph= get_complex_graph(
            axes,
            lambda x: A * np.exp(1j *(k*x-w*t))
        )
        self.add(graph)
