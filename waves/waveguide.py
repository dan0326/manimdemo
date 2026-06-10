from manimlib_import_ext import *
import numpy as np


class WaveguideStandingWave(InteractiveScene):
    def construct(self):
        # 1. Setup 3D Axes
        axes = ThreeDAxes()
        # self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        # 2. Parameters for the Waveguide
        a = 4  # Width (x-direction)
        L = 6  # Length (z-direction)

        # 3. Create the Plates (Top and Bottom)
        top_plate = Rectangle(width=L, height=a, fill_opacity=0.2, color=GREY)
        top_plate.rotate(90 * DEGREES, axis=RIGHT)
        top_plate.shift(UP * 1.5)

        bottom_plate = top_plate.copy().shift(DOWN * 3)
        self.add(top_plate, bottom_plate)

        # 4. Time Tracker for the oscillation
        time = ValueTracker(0)
        self.add(time)

        # 5. Create the Standing Wave Surface
        # This surface represents the E-field intensity
        def get_wave_surface():
            t = time.get_value()
            surface = ParametricSurface(
                lambda u, v: np.array([
                    # x-axis (transverse)
                    u,
                    # Sin profile across plates
                    1.5 * np.sin(PI * (u + a/2) / a) *
                    np.sin(PI * (v + L/2) / L) *  # Sin profile along waveguide
                    # Temporal oscillation
                    np.cos(2 * t),
                    # z-axis (longitudinal)
                    v
                ]),
                u_range=[-a/2, a/2],
                v_range=[-L/2, L/2],
                color=BLUE,
                opacity=0.8
            )
            # surface.set_style(fill_opacity=0.5, stroke_width=1)
            return surface

        standing_wave = always_redraw(get_wave_surface)

        # 6. Animation
        title = Text("Waveguide Resonant Cavity (Standing Wave)", font_size=24)
        title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)

        self.add(standing_wave)

        # Animate the oscillation (standing wave "breathing")
        self.play(
            time.animate.set_value(2 * PI),
            run_time=6,
            rate_func=linear
        )
        self.wait()
