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

def get_complex_vector(plane, z, color=YELLOW):
    z_vect = Vector()
    z_vect.put_start_and_end_on(plane.n2p(0), plane.n2p(z))
    z_vect.rotate(TAU/4, axis=z_vect.get_vector())
    z_vect.set_color(color)
    return z_vect

class SchrodingerPlay(InteractiveScene):
    def construct(self):
        #axes
        x_max=3
        axes= ThreeDAxes(
            x_range=(0, 10),
            y_range=(-x_max, x_max),
            z_range=(-x_max, x_max),
            width = 10,
            height=6,
            depth=6
        )
        self.add(axes)

        #add complex plane
        planes=VGroup()
        for x in range(1, 10):
            plane = ComplexPlane(
                (-x_max, x_max), (-x_max, x_max),
                background_line_style=dict(stroke_color=BLUE, stroke_width=1, stroke_opacity=1),
                faded_line_style=dict(stroke_color=BLUE,stroke_width=1, stroke_opacity=0.5),
                height=6,
                width=6
            )
            plane.rotate(90 * DEGREES, RIGHT)
            plane.rotate(90 * DEGREES, OUT)
            plane.move_to(axes.c2p(x, 0, 0))
            planes.add(plane)
        plane= planes[2]
        self.add(plane)
        self.frame.reorient(45, 88, 0, (np.float32(0.0), np.float32(0.23), np.float32(0.49)), 8.00)

        #show graph of one solution
        A=1
        k=0.5
        w=1
        t_tracker = ValueTracker(0)
        get_t = t_tracker.get_value
        time_label = Tex("{time = 0.00}")
        time_label.to_corner(UR)
        time_label.fix_in_frame()
        time_value = time_label.make_number_changeable("0.00")
        time_value.fix_in_frame()
        time_value.add_updater(lambda m: m.set_value(get_t()))
        self.add(time_label)
        def plane_wave(x):
            t = get_t()
            return A * np.exp(1j *(k*x-w*t))
        graph= always_redraw(lambda: get_complex_graph(axes, plane_wave))
        self.add(graph)
        self.play(t_tracker.animate.set_value(3), run_time = 3, rate_func = linear)

        #add solutioin arrow on one plane
        x=axes.x_axis.p2n(plane.get_center())
        z_vect = get_complex_vector(plane, plane_wave(x))
        z_dot = GlowDot()
        z_dot.f_always.move_to(lambda: z_vect.get_end())
        self.add(z_vect)
        self.add(z_dot)

        #add laplacian and difference vector
        def laplacian(x):
            return -1 *(k**2) * plane_wave(x)
        def ddt_psi(x):
            return -1j * laplacian(x)
        l_vect = get_complex_vector(plane, laplacian(x), color=BLUE)
        dt_vect = get_complex_vector(plane, ddt_psi(x), color=YELLOW)
        self.play(
            self.frame.animate.reorient(71, 77, 0, (np.float32(-0.63), np.float32(-0.27), np.float32(0.61)), 3.38),
            run_time =2)
        self.play(GrowArrow(l_vect))
        self.wait()
        self.play(TransformFromCopy(l_vect, dt_vect))
        self.wait()
        self.add(dt_vect)


