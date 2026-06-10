from manimlib import *
import numpy as np

class RotatingTriangle(Scene):
    def construct(self):
        # Define the vertices of an equilateral triangle
        vertex_a = np.array([0, 0, 0])
        vertex_b = np.array([2, 0, 0])
        vertex_c = np.array([1, np.sqrt(3), 0])
        
        # Create the triangle using the vertices
        triangle = Polygon(vertex_a, vertex_b, vertex_c)
        triangle.set_fill(BLUE, opacity=0.5)
        triangle.set_stroke(WHITE, width=2)
        
        # Create a dot at the top vertex for tracing (stays with the triangle)
        top_dot = Dot(vertex_c, color=RED)
        triangle.add(top_dot)
        
        # Create the traced path of the top dot
        trace = TracedPath(top_dot.get_center, stroke_color=RED)
        
        # Create the square attached along the base of the triangle (it remains static)
        square = Polygon(
            vertex_a,
            vertex_b,
            vertex_b + np.array([0, -2, 0]),
            vertex_a + np.array([0, -2, 0])
        )
        square.set_fill(GREEN, opacity=0.5)
        square.set_stroke(WHITE, width=2)
        
        # Display the initial objects
        self.add(trace, triangle, square)
        self.wait(1)
        
        # We'll now rotate the triangle in 12 steps (30° increments).
        # At each step, we add a permanently-filled copy of the triangle.
        snapshots = VGroup()
        # Save the initial triangle (0°) snapshot
        snapshot = triangle.copy()
        snapshots.add(snapshot)
        self.add(snapshot)
        
        rotation_angle = TAU / 12  # 30 degrees per step

        for i in range(1, 13):
            self.play(
                Rotate(triangle, angle=rotation_angle, about_point=vertex_a, run_time=0.5, rate_func=linear)
            )
            # Make a snapshot of the triangle at this angle and add it permanently.
            snapshot = triangle.copy()
            snapshot.set_fill(BLUE, opacity=0.5)
            snapshots.add(snapshot)
            self.add(snapshot)
            self.wait(0.2)
        
        # Optionally, remove the actively rotating triangle so that only the snapshots remain.
        self.remove(triangle)
        self.wait(2)