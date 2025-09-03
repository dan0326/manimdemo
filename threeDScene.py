from manimlib import *
import numpy as np

class UpperHalfSphere(ThreeDScene):
    def construct(self):
        # camera orientation (ManimGL)
        self.frame.set_phi = np.deg2rad(65)
        self.frame.set_theta = np.deg2rad(45)
        
        # Axes for reference
        x_max = 10
        y_max = 10
        axes = ThreeDAxes(
            x_range=(-x_max, x_max, 1),
            y_range=(-y_max, y_max, 1),
            z_range=(0, 5, 1),
        )
        self.add(axes)

        # Add a line segment
        line = Line(ORIGIN, axes.c2p(2, 3, 4), color=RED)
        #self.add(line)

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
        #self.add(sphere)

        #test plane1
        plane1 = ParametricSurface(
            lambda u, v: np.array([u,v, 1-u-v]),
            u_range=(-5, 5),
            v_range=(-5, 5),
            resolution=(30, 30),
            color=YELLOW_E,
            opacity=0.4,
        )
        plane1.set_color_by_xyz_func("z", colormap="turbo")
        self.add(plane1)

        #plane 1 prime
        planeh = ParametricSurface(
            lambda u, v: (u, v, 5+u-v),
            u_range=(-5, 5),
            v_range=(-5, 5),
            resolution = (30, 30),
            opacity=0.5)
        planeh.set_color_by_xyz_func("z")
        self.add(planeh)

        #add plane2 along with its mesh
        plane2 = ParametricSurface(
            lambda u, v: np.array([u, v, (u**2+v**2)*np.exp(-u)]),
            u_range=(-10, 10),
            v_range=(-10, 10),
            color = BLUE,
            opacity=0.8)
        surface2 = SurfaceMesh(plane2,
            resolution=(30, 30), 
            stroke_width=1,
            stroke_color=GREY_A)
        surfaceWmesh2 = Group(plane2, surface2)
        plane2.set_color_by_xyz_func("z")
        self.add(surfaceWmesh2)

        #add plane3
        plane3 = ParametricSurface(
            lambda u,v : np.array([u, v, np.sin(u-v)/(np.abs(u)+np.abs(v))]),
            u_range=(-10, 10),
            v_range=(-10, 10),
            color = BLUE,
            opacity=0.8)
        surface3 = SurfaceMesh(plane3,
            resolution=(30, 30),
            stroke_width=1,
            stroke_color=GREY_C)
        surfaceWmesh3 = Group(plane3, surface3)
        plane3.set_color_by_xyz_func("z", min_value=-10, max_value=10)
        self.add(surfaceWmesh3)

        self.play(ReplacementTransform(surfaceWmesh2, surfaceWmesh3))

        

        self.camera.get_location()
