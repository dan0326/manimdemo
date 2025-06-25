from manimlib import *
import numpy as np

class UpperHalfSphere(ThreeDScene):
    def construct(self):
        # Axes for reference
        axes = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            z_range=[0, 5, 1],
        )

        # Parametric surface: u=polar angle [0, π/2], v=azimuthal [0, 2π]
        sphere = ParametricSurface(
            lambda u, v: np.array([
                np.sin(u) * np.cos(v),
                np.sin(u) * np.sin(v),
                np.cos(u)
            ]),
            u_range=[0, PI/2],
            v_range=[0, 2*PI],
            resolution=(30, 60),
            color=BLUE_E
        )

        plane1 = ParametricSurface(
            lambda u, v: np.array([u,v, 1-u-v]),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(30, 30),
            color=YELLOW_E,
            opacity=0.5,
        )

        line = Line3D(
            start=np.array([-2, -2, 3]),
            end=np.array([2, 2, 0]),
            color=RED
        )

        # camera orientation (ManimGL)
        self.camera.phi = np.deg2rad(65)
        self.camera.theta = np.deg2rad(45)

        # add and animate
        self.add(axes, sphere, plane1, line)