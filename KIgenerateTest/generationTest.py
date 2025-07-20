from manimlib import *

class MainScene(ThreeDScene):
    def construct(self):
        
        # Create axes
        axes = ThreeDAxes()
        
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

        # Create the mesh for the surface
        surface_mesh = SurfaceMesh(
            surface,
            resolution=(30, 30),
            stroke_width=1.5,
            stroke_color=GREY_C
        )

        # Group them for easier manipulation
        surface_with_mesh = Group(surface, surface_mesh)
        
        # Add custom labels
        x_label = Tex("x").next_to(axes.x_axis.get_end(), RIGHT)
        y_label = Tex("y").next_to(axes.y_axis.get_end(), UP)
        z_label = Tex("z").next_to(axes.z_axis.get_end(), OUT)
        
        # Create animations
        self.play(ShowCreation(axes), Write(x_label), Write(y_label), Write(z_label))
        self.play(ShowCreation(surface_with_mesh))
        self.wait(2)
