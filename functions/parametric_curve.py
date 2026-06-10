from manimlib import *
from manimlib.utils import color

class parametric_scene(InteractiveScene):
    def construct(self):
        axes_3d = ThreeDAxes()
        curve1 = ParametricCurve(
            lambda t: [
                np.cos(t),
                np.sin(t),
                np.log(np.cos(t))
                ],
            t_range=(0, PI/4, 0.01),
            color=RED
            )
        self.add(axes_3d,curve1)
        self.frame.get_implied_camera_location()
