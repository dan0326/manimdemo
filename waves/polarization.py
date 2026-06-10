from manimlib_import_ext import *


class LinearPolarizationScene(InteractiveScene):
    def construct(self):
        # Configuration
        x_range = (0, 10)
        y_range = (-2, 2)
        z_range = (-2, 2)

        # 1. Create Axes
        axes = ThreeDAxes(
            x_range=(x_range[0], x_range[1], 1),
            y_range=(y_range[0], y_range[1], 1),
            z_range=(z_range[0], z_range[1], 1),
            width=10,
            height=6,
            depth=6
        )
        self.add(axes)

        # 2. Setup Trackers
        t_tracker = ValueTracker(0)
        get_t = t_tracker.get_value

        # Constants
        A = 1.5
        k = 2 * PI / 4  # wavelength = 4
        w = 1.0

        def get_E_field(x, t):
            phase = w * t - k * x
            # Linearly polarized in Y direction
            return np.array([0, A * np.cos(phase), 0])

        def get_B_field(x, t):
            phase = w * t - k * x
            # B is perpendicular to E and k (x-axis)
            # E = (0, Ey, 0) -> B = (0, 0, Ey)
            return np.array([0, 0, A * np.cos(phase)])

        # 3. Create the Wave Curves
        def get_wave_curve(field_func, color=YELLOW, opacity=0.8):
            xs = np.linspace(x_range[0], x_range[1], 200)
            t = get_t()
            points = [axes.c2p(x, *field_func(x, t)[1:]) for x in xs]
            curve = VMobject()
            curve.set_points_smoothly(points)
            curve.set_stroke(color=color, width=4, opacity=opacity)
            return curve

        e_curve = always_redraw(
            lambda: get_wave_curve(get_E_field, color=YELLOW))
        b_curve = always_redraw(
            lambda: get_wave_curve(get_B_field, color=BLUE))

        self.add(e_curve, b_curve)

        def get_field_vector(x, field_func, color):
            t = get_t()
            field = field_func(x, t)
            start = axes.c2p(x, 0, 0)
            end = axes.c2p(x, field[1], field[2])
            vec = Arrow(start, end, buff=0, color=color)
            return vec

        # 4. Add Vectors
        num_vectors = 20
        x_values = np.linspace(x_range[0], x_range[1], num_vectors)

        for x in x_values:
            self.add(always_redraw(
                lambda x=x: get_field_vector(x, get_E_field, YELLOW)))
            self.add(always_redraw(
                lambda x=x: get_field_vector(x, get_B_field, BLUE)))

        # 5. Rotating Plane at x=0
        plane = ComplexPlane(
            (-2, 2), (-2, 2),
            background_line_style=dict(
                stroke_color=GREY, stroke_width=1, stroke_opacity=0.3),
        )
        plane.rotate(90 * DEGREES, UP)
        plane.move_to(axes.c2p(0, 0, 0))
        self.add(plane)

        # 6. Labels and Animation
        self.frame.reorient(1, 70, 0, (0.71, 1.5, 0.61), 10.00)

        labels = VGroup(
            Tex(r"\text{Linear Polarization}", color=WHITE),
            Tex(r"\text{Electric Field } \mathbf{E}", color=YELLOW),
            Tex(r"\text{Magnetic Field } \mathbf{B}", color=BLUE)
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UL).fix_in_frame()
        self.add(labels)

        self.play(t_tracker.animate.set_value(
            TAU * 4), run_time=20, rate_func=linear)


class EllipticalPolarizationScene(InteractiveScene):
    def construct(self):
        # Configuration
        x_range = (0, 10)
        y_range = (-2, 2)
        z_range = (-2, 2)

        axes = ThreeDAxes(
            x_range=(x_range[0], x_range[1], 1),
            y_range=(y_range[0], y_range[1], 1),
            z_range=(z_range[0], z_range[1], 1),
            width=10, height=6, depth=6
        )
        self.add(axes)

        t_tracker = ValueTracker(0)
        get_t = t_tracker.get_value

        # Constants for Elliptical (Different amplitudes)
        Ay = 1.5
        Az = 0.8
        k = 2 * PI / 4
        w = 1.0

        def get_E_field(x, t):
            phase = w * t - k * x
            return np.array([0, Ay * np.cos(phase), Az * np.sin(phase)])

        def get_B_field(x, t):
            phase = w * t - k * x
            # B = (0, -Ez, Ey) * scale (ignoring 1/c scale for visualization)
            return np.array([0, -Az * np.sin(phase), Ay * np.cos(phase)])

        def get_wave_curve(field_func, color=YELLOW):
            xs = np.linspace(x_range[0], x_range[1], 200)
            t = get_t()
            points = [axes.c2p(x, *field_func(x, t)[1:]) for x in xs]
            curve = VMobject().set_points_smoothly(points)
            curve.set_stroke(color=color, width=4)
            return curve

        self.add(always_redraw(lambda: get_wave_curve(get_E_field, YELLOW)))
        self.add(always_redraw(lambda: get_wave_curve(get_B_field, BLUE)))

        num_vectors = 20
        x_values = np.linspace(x_range[0], x_range[1], num_vectors)
        for x in x_values:
            self.add(always_redraw(lambda x=x: Arrow(axes.c2p(x, 0, 0), axes.c2p(
                x, *get_E_field(x, get_t())[1:]), buff=0, color=YELLOW)))
            self.add(always_redraw(lambda x=x: Arrow(axes.c2p(x, 0, 0), axes.c2p(
                x, *get_B_field(x, get_t())[1:]), buff=0, color=BLUE)))

        plane = ComplexPlane(
            (-2, 2), (-2, 2),
            background_line_style=dict(
                stroke_color=GREY, stroke_width=1, stroke_opacity=0.3),
        )
        plane.rotate(90 * DEGREES, UP)
        plane.move_to(axes.c2p(0, 0, 0))
        self.add(plane)

        self.frame.reorient(1, 70, 0, (0.71, 1.5, 0.61), 10.00)

        labels = VGroup(
            Tex(r"\text{Elliptical Polarization}", color=WHITE),
            Tex(r"E_y = A_y \cos(\omega t - kx)", color=YELLOW),
            Tex(r"E_z = A_z \sin(\omega t - kx)", color=YELLOW),
            # Tex(r"A_y \neq A_z", color=RED)
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UL).fix_in_frame()
        self.add(labels)

        self.play(t_tracker.animate.set_value(
            TAU * 4), run_time=20, rate_func=linear)


class CircularPolarizationScene(InteractiveScene):
    def construct(self):
        # Configuration
        x_range = (0, 10)
        y_range = (-2, 2)
        z_range = (-2, 2)

        # 1. Create Axes
        axes = ThreeDAxes(
            x_range=(x_range[0], x_range[1], 1),
            y_range=(y_range[0], y_range[1], 1),
            z_range=(z_range[0], z_range[1], 1),
            width=10,
            height=6,
            depth=6
        )
        self.add(axes)

        # 2. Setup Trackers
        t_tracker = ValueTracker(0)
        get_t = t_tracker.get_value

        # Constants
        A = 1.5
        k = 2 * PI / 4  # wavelength = 4
        w = 1.0

        def get_E_field(x, t):
            phase = w * t - k * x
            return np.array([0, A * np.cos(phase), A * np.sin(phase)])

        def get_B_field(x, t):
            phase = w * t - k * x
            # B is perpendicular to E and k (x-axis)
            # B = 1/c (k_hat x E)
            # E = (0, Ey, Ez) -> B = (0, -Ez, Ey)
            return np.array([0, -A * np.sin(phase), A * np.cos(phase)])

        # 3. Create the Wave Curves (Helixes)
        def get_wave_curve(field_func, color=YELLOW, opacity=0.8):
            xs = np.linspace(x_range[0], x_range[1], 200)
            t = get_t()
            points = [axes.c2p(x, *field_func(x, t)[1:]) for x in xs]
            curve = VMobject()
            curve.set_points_smoothly(points)
            curve.set_stroke(color=color, width=4, opacity=opacity)
            return curve

        e_curve = always_redraw(
            lambda: get_wave_curve(get_E_field, color=YELLOW))
        b_curve = always_redraw(
            lambda: get_wave_curve(get_B_field, color=BLUE))

        # 4. Add components
        def get_component_curve(field_func, component_idx, color, opacity=0.5):
            xs = np.linspace(x_range[0], x_range[1], 200)
            t = get_t()
            points = []
            for x in xs:
                field = field_func(x, t)
                comp_vec = [0, 0, 0]
                comp_vec[component_idx] = field[component_idx]
                points.append(axes.c2p(x, *comp_vec[1:]))
            curve = VMobject()
            curve.set_points_smoothly(points)
            curve.set_stroke(color=color, width=2, opacity=opacity)
            return curve

        ey_curve = always_redraw(
            lambda: get_component_curve(get_E_field, 1, YELLOW_E, 0.3))
        ez_curve = always_redraw(
            lambda: get_component_curve(get_E_field, 2, YELLOW_E, 0.3))

        self.add(e_curve, b_curve)
        self.add(ey_curve, ez_curve)

        def get_field_vector(x, field_func, color, label_text):
            t = get_t()
            field = field_func(x, t)
            start = axes.c2p(x, 0, 0)
            end = axes.c2p(x, field[1], field[2])
            vec = Arrow(start, end, buff=0, color=color)
            return vec

        # 5. Add Vectors at multiple points
        num_vectors = 20
        x_values = np.linspace(x_range[0], x_range[1], num_vectors)

        e_vectors = VGroup()
        b_vectors = VGroup()

        for x in x_values:
            e_vec = always_redraw(lambda x=x: get_field_vector(
                x, get_E_field, YELLOW, "E"))
            b_vec = always_redraw(
                lambda x=x: get_field_vector(x, get_B_field, BLUE, "B"))
            e_vectors.add(e_vec)
            b_vectors.add(b_vec)

        self.add(e_vectors, b_vectors)

        # 6. Rotating Plane at x=0
        plane = ComplexPlane(
            (-2, 2), (-2, 2),
            background_line_style=dict(
                stroke_color=GREY, stroke_width=1, stroke_opacity=0.3),
        )
        plane.rotate(90 * DEGREES, UP)
        plane.move_to(axes.c2p(0, 0, 0))
        self.add(plane)

        # 7. Animation
        self.frame.reorient(1, 70, 0, (0.71, 1.5, 0.61), 10.00)

        # Add labels
        labels = VGroup(
            Tex(r"\text{Circular Polarization}", color=WHITE),
            Tex(r"\text{Electric Field } \mathbf{E}", color=YELLOW),
            Tex(r"\text{Magnetic Field } \mathbf{B}", color=BLUE)
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UL).fix_in_frame()

        wave_equation = Tex(
            r"\nabla^2 \mathbf{E} = \frac{1}{c^2} \frac{\partial^2 \mathbf{E}}{\partial t^2}",
            color=WHITE
        ).to_corner(UR).fix_in_frame()

        self.add(labels, wave_equation)

        self.play(
            t_tracker.animate.set_value(TAU * 4),
            run_time=20,
            rate_func=linear
        )
        self.wait()
