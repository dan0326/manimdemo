from manimlib_import_ext import *

class GaussianDist(InteractiveScene):
    def construct(self):
        self.frame.reorient(51, 73, 0, (np.float32(0.0), np.float32(0.0), np.float32(0.0)), 8.00)
        
        # Axes for reference
        x_max = 10
        y_max = 10
        axes = ThreeDAxes(
            x_range=(-x_max, x_max, 1),
            y_range=(-y_max, y_max, 1),
            z_range=(0, 5, 1),
        )
        self.play(Write(axes), run_time = 2)

        #add graph
        ripple = ParametricSurface(
            lambda u, v: (u, v, np.exp(-u**2 -v**2)), 
            u_range=(-5, 5),
            v_range=(-5, 5),
            resolution = (100, 100),
            opacity= 0.9)
        ripple.set_color_by_xyz_func("z",
            min_value=0,
            max_value=2)
        mesh4ripple = SurfaceMesh(ripple, stroke_width=0.5, depth_test=False,
            resolution=(20, 20))
        self.add(ripple)
        self.add(mesh4ripple)
        self.play(self.frame.animate.reorient(133, 72, 0, (np.float32(0.0), np.float32(0.0), np.float32(0.0)), 8.00),
            run_time=5)
        