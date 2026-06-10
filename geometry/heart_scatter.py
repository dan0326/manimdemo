import random
from manimlib_import_ext import *


class HeartShape(InteractiveScene):
    def construct(self):

        # Get from the scene's camera frame  
        frame = self.camera.frame  
        width = frame.get_width()  
        height = frame.get_height()  
        center = frame.get_center()  
          
        # Calculate boundaries  
        min_x = center[0] - width/2  
        max_x = center[0] + width/2  
        min_y = center[1] - height/2  
        max_y = center[1] + height/2

        #add axes
        axes = Axes()
        self.add(axes)
        
        def draw_heart(center):
            heart = ParametricCurve(
                lambda t: np.array([
                    16 * np.sin(t)**3,
                    13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t),
                    0
                ]),
                t_range=[0, TAU, 0.1],
                color=RED
            )
            # Scale it down because the raw values are quite large
            heart.scale(0.1)
            heart.move_to(center, aligned_edge=DOWN)
            return heart

        # draw a clover test
        cloves = VGroup()

        self.frame.reorient(0, 0, 0, (-0.01, -0.32, 0.0), 25.91)

        def draw_clove(clove_center):
            heart1 = draw_heart(clove_center)
            self.add(heart1)
            heart2 = heart1.copy()
            self.add(heart2)
            heart1.rotate(-90 * DEGREES, about_point=clove_center)
            heart3 = heart1.copy()
            self.add(heart3)
            heart1.rotate(-90 * DEGREES, about_point=clove_center)
            heart4 = heart1.copy()
            self.add(heart4)
            heart1.rotate(-90 * DEGREES, about_point=clove_center)
            clove = VGroup(heart1, heart2, heart3, heart4)
            return clove

        for _ in range(6):
            random_x = random.uniform(min_x, max_x)
            random_y = random.uniform(min_y, max_y)
            center = (random_x, random_y, 0)
            draw_clove(center)

