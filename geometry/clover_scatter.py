import random
import numpy as np
from manimlib_import_ext import *

class HeartShape(InteractiveScene):
    def construct(self):
        # Get from the scene's camera frame
        self.frame.reorient(0, 0, 0, (-0.01, -0.32, 0.0), 25.91)
        frame = self.camera.frame  
        width = frame.get_width()  
        height = frame.get_height()  
        center_f = frame.get_center()
          
        # Calculate boundaries (with a bit of padding so they don't go off-screen)
        padding = 2
        min_x, max_x = center_f[0] - width/2 + padding, center_f[0] + width/2 - padding
        min_y, max_y = center_f[1] - height/2 + padding, center_f[1] + height/2 - padding
        
        def get_heart(center_point):
            heart = ParametricCurve(
                lambda t: np.array([
                    16 * np.sin(t)**3,
                    13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t),
                    0
                ]),
                t_range=[0, TAU, 0.1],
                color= "#FF99E5"
            )
            heart.scale(0.08) # Slightly smaller to fit 4 better
            heart.set_stroke(width=1)
            # Move heart so its tip is at the center_point
            heart.move_to(center_point, aligned_edge=DOWN)
            heart.set_fill("#FFB5B5", opacity=0.75)
            return heart

        def get_clove(clove_center):
            # Create 4 hearts rotated around the center
            hearts = VGroup()
            for i in range(4):
                h = get_heart(clove_center)
                h.rotate(i * -90 * DEGREES, about_point=clove_center)
                hearts.add(h)
            return hearts

        # Keep track of active clovers
        active_clovers = []

        for _ in range(8):
            random_x = random.uniform(min_x, max_x)
            random_y = random.uniform(min_y, max_y)
            pos = np.array([random_x, random_y, 0])
            
            # Create the clover mobject
            new_clove = get_clove(pos)            

            if len(active_clovers) >= 2:
                oldest = active_clovers.pop(0)
                self.play(
                    FadeOut(oldest),
                    Write(new_clove),
                    run_time=2
                )
            else:
                # Just add the new one if screen is empty or has only 1
                self.play(Write(new_clove), run_time=2)
            
            active_clovers.append(new_clove)
            self.wait(0.5)

        self.wait(2)

