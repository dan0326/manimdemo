from manimlib import *
import numpy as np

class TriangleSquareRotation(Scene):
    def construct(self):
        # Define vertices of the equilateral triangle
        vertex_a = np.array([0, 0, 0])
        vertex_b = np.array([2, 0, 0])
        vertex_c = np.array([1, np.sqrt(3), 0])
        triangle = Polygon(vertex_a, vertex_b, vertex_c)
        triangle.set_fill(BLUE, opacity=0.5)
        triangle.set_stroke(WHITE, width=2)

        # Create a square attached to the triangle's bottom (using its base as the top edge)
        square = Polygon(
            vertex_a,
            vertex_b,
            vertex_b + np.array([0, -2, 0]),
            vertex_a + np.array([0, -2, 0])
        )
        square.set_fill(GREEN, opacity=0.5)
        square.set_stroke(WHITE, width=2)

        # Display the initial objects
        self.add(triangle, square)
        self.wait(1)

        # Start with a red dot on the triangle's top vertex and a trace.
        top_dot = Dot(vertex_c, color=RED)
        triangle.add(top_dot)
        trace = TracedPath(top_dot.get_center, stroke_color=RED)
        self.add(trace)

        # Create a copy of the triangle to track its initial state for filling the swept area later
        initial_triangle = triangle.copy()
        

        # First rotation with synchronized swept-area fill
        sweep_tracker = ValueTracker(0)
        radius = np.linalg.norm(vertex_c - vertex_a)
        start_angle = np.arctan2((vertex_c - vertex_a)[1], (vertex_c - vertex_a)[0])
        swept_area = always_redraw(lambda: Sector(
            angle=sweep_tracker.get_value(),
            radius=radius,
            start_angle=start_angle,
            arc_center=vertex_a
        ).set_fill(YELLOW, opacity=0.5).set_stroke(WHITE, width=1))
        self.add(swept_area)
        self.play(
            Rotate(triangle, angle=210 * DEGREES, about_point=vertex_a),
            sweep_tracker.animate.set_value(210 * DEGREES),
            run_time=1
        )
        
        self.play(FadeOut(top_dot), run_time=0.5)
        triangle.remove(top_dot)
        # Snapshot 1: the triangle’s first position
        snapshot1 = triangle.copy()
        self.add(snapshot1)

        # Second rotation: add new dot and rotate around vertex_a + [0, -2, 0]
        top_dot = Dot(np.array([-np.sqrt(3), -1, 0]), color=RED)
        triangle.add(top_dot)
        trace = TracedPath(top_dot.get_center, stroke_color=RED)
        self.add(trace)
        self.play(
            Rotate(triangle, angle=210 * DEGREES, about_point=vertex_a + np.array([0, -2, 0]), run_time=1)
        )
        self.play(FadeOut(top_dot), run_time=0.5)
        triangle.remove(top_dot)
        # Snapshot 2: the triangle’s second position
        snapshot2 = triangle.copy()
        self.add(snapshot2)

        # Third rotation: add new dot and rotate around vertex_b + [0, -2, 0]
        top_dot = Dot(np.array([1, -2 - np.sqrt(3), 0]), color=RED)
        triangle.add(top_dot)
        trace = TracedPath(top_dot.get_center, stroke_color=RED)
        self.add(trace)
        self.play(
            Rotate(triangle, angle=210 * DEGREES, about_point=vertex_b + np.array([0, -2, 0]), run_time=1)
        )
        self.play(FadeOut(top_dot), run_time=0.5)
        triangle.remove(top_dot)
        # Snapshot 3: the triangle’s third position
        snapshot3 = triangle.copy()
        self.add(snapshot3)

        # Fourth rotation: add new dot and rotate around vertex_b
        top_dot = Dot(np.array([2 + np.sqrt(3), -1, 0]), color=RED)
        triangle.add(top_dot)
        trace = TracedPath(top_dot.get_center, stroke_color=RED)
        self.add(trace)
        self.play(
            Rotate(triangle, angle=150 * DEGREES, about_point=vertex_b)
        )
        #self.play(FadeOut(top_dot), run_time=0.5)
        triangle.remove(top_dot)

        self.play(
            Rotate(triangle, angle=60 * DEGREES, about_point=vertex_b)
        )
        # Snapshot 4: the triangle’s fourth position
        snapshot4 = triangle.copy()
        self.add(snapshot4)

        #self.embed()
