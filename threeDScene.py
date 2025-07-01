from manimlib import *
from manimlib.utils import color
import numpy as np

class UpperHalfSphere(ThreeDScene):
    def construct(self):
        # camera orientation (ManimGL)
        self.camera.phi = np.deg2rad(65)
        self.camera.theta = np.deg2rad(45)
        
        # Axes for reference
        x_max = 10
        y_max = 10
        axes = ThreeDAxes(
            x_range=(-x_max, x_max, 1),
            y_range=(-y_max, y_max, 1),
            z_range=(0, 5, 1),
        )
        self.add(axes)

        # Parametric surface: u=polar angle [0, π/2], v=azimuthal [0, 2π]
        sphere = ParametricSurface(
            lambda u, v: np.array([
                np.sin(u) * np.cos(v),
                np.sin(u) * np.sin(v),
                np.cos(u)
            ]),
            u_range=(0, PI/2),
            v_range=(0, 2*PI),
            resolution=(30, 60),
            color=BLUE_E,
            opacity=0.5
        )
        self.add(sphere)

        plane1 = ParametricSurface(
            lambda u, v: np.array([u,v, 1-u-v]),
            u_range=(-2, 2),
            v_range=(-2, 2),
            resolution=(30, 30),
            color=YELLOW_E,
            opacity=0.5,
        )
        self.add(plane1)

        #add another plane
        plane2 = ParametricSurface(
            lambda u, v: np.array([u, v, (u**2+v**2)*np.exp(-u)]),
            u_range=(-10, 10),
            v_range=(-10, 10),
            color = BLUE,
            opacity=0.8)
        self.add(plane2)

        # Add a line segment
        line = Line(ORIGIN, axes.c2p(2, 3, 4), color=RED)
        self.add(line)
