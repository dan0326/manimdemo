from manimlib import *

class MainScene(ThreeDScene):
    def construct(self):
        
        # Create axes
        axes = ThreeDAxes()
        x_label = Tex("x").next_to(axes.x_axis.get_end(), RIGHT)
        y_label = Tex("y").next_to(axes.y_axis.get_end(), UP)
        z_label = Tex("z").next_to(axes.z_axis.get_end(), OUT)
        z_label.rotate(90 *DEGREES, RIGHT)
        self.play(ShowCreation(axes), Write(x_label), Write(y_label), Write(z_label), run_time=2)
        
        # Create surface
        def func(x, y):
            return np.sin(x) * np.cos(y) 
        surface = ParametricSurface(
            lambda u, v: axes.c2p(u, v, func(u, v)),
            u_range=[-3, 3],
            v_range=[-3, 3],
            color=BLUE_E,
            opacity=0.8
            )
        surface.set_color_by_xyz_func("z", min_value=-1, max_value=1, colormap="turbo")
        self.play(ShowCreation(surface), run_time=2)

        # Create the mesh for the surface
        surface_mesh = SurfaceMesh(
            surface,
            resolution=(30, 30),
            stroke_width=1,
            stroke_color=GREY_B
        )
        self.add(surface_mesh)

        # Group them for easier manipulation
        surface_with_mesh = Group(surface, surface_mesh)

        self.wait(2)
