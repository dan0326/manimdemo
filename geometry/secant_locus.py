from manimlib import *
import numpy as np

class SecantLocusScene(Scene):
    def construct(self):
        # 1. Setup Coordinate System
        # Since the circle is centered at (5, -6) with r=10, 
        # we need a large view.
        axes = NumberPlane(
            x_range=(-10, 20, 2),
            y_range=(-20, 10, 2),
            background_line_style={
                "stroke_color": GREY_D,
                "stroke_width": 1.5,
                "stroke_opacity": 0.5
            }
        )
        self.add(axes)
        
        # Adjust camera to see the relevant area
        self.camera.frame.set_width(35)
        self.camera.frame.move_to(np.array([5, -6, 0]))

        # 2. Define key points and geometry
        center_coords = np.array([5, -6, 0])
        p_coords = np.array([1, 2, 0])
        radius = 10
        
        main_circle = Circle(radius=radius, color=BLUE)
        main_circle.move_to(center_coords)
        
        point_o = Dot(center_coords, color=WHITE)
        label_o = Text("O(5,-6)", font_size=48).next_to(point_o, DOWN)
        
        point_p = Dot(p_coords, color=RED)
        label_p = Text("P(1,2)", font_size=48).next_to(point_p, UR, buff=0.1)

        diameter_line = Line((1, 2, 0), (5, -6, 0), color = BLUE)
        
        self.add(main_circle, point_o, label_o, point_p, label_p, diameter_line)
        
        # 3. Locus calculation (The "Little Circle")
        # The locus of midpoints M of chords through P is a circle 
        # with diameter OP.
        mid_op = (center_coords + p_coords) / 2
        dist_op = np.linalg.norm(center_coords - p_coords)
        locus_circle = Circle(radius=dist_op/2, color=YELLOW)
        locus_circle.move_to(mid_op)
        
        # 4. Dynamic Secant Line and Midpoint
        angle_tracker = ValueTracker(0)
        
        def get_secant_line():
            angle = angle_tracker.get_value()
            direction = np.array([np.cos(angle), np.sin(angle), 0])
            # A long line through P
            line = Line(p_coords - direction * 15, p_coords + direction * 15, color=GREY_A)
            line.set_stroke(opacity=0.5)
            return line

        def get_chord_and_midpoint():
            angle = angle_tracker.get_value()
            u = np.array([np.cos(angle), np.sin(angle), 0])
            
            # Intersection of Line: P + t*u with Circle: |X - O|^2 = R^2
            # |P - O + t*u|^2 = R^2
            # Let V = P - O
            # |V + t*u|^2 = R^2 => t^2 + 2t(V·u) + |V|^2 - R^2 = 0
            v = p_coords - center_coords
            v_dot_u = np.dot(v, u)
            v_mag_sq = np.dot(v, v)
            
            discriminant = v_dot_u**2 - (v_mag_sq - radius**2)
            if discriminant < 0:
                return VGroup() # Should not happen if P is inside
            
            t1 = -v_dot_u + np.sqrt(discriminant)
            t2 = -v_dot_u - np.sqrt(discriminant)
            
            a = p_coords + t1 * u
            b = p_coords + t2 * u
            midpoint = (a + b) / 2
            
            chord = Line(a, b, color=YELLOW, stroke_width=4)
            m_dot = Dot(midpoint, color=YELLOW)
            
            # Perpendicular from O to chord
            perp_line = Line(center_coords, midpoint, color=WHITE, stroke_width=2)
            
            # Manually construct RightAngle mark
            # s is the size of the mark
            s = 0.2
            # Unit vector along the chord (u) and along the perpendicular (w)
            # w points from midpoint back to center O
            dist_mo = np.linalg.norm(center_coords - midpoint)
            if dist_mo > 0.001:
                w = (center_coords - midpoint) / dist_mo
                # Points for the right angle elbow
                p1 = midpoint + s * u
                p2 = midpoint + s * u + s * w
                p3 = midpoint + s * w
                ra = VMobject(color=WHITE, stroke_width=2)
                ra.set_points_as_corners([p1, p2, p3])
            else:
                ra = VGroup() # At the center, the angle is undefined
            
            return VGroup(chord, m_dot, perp_line, ra)

        secant_line = always_redraw(get_secant_line)
        chord_group = always_redraw(get_chord_and_midpoint)
        
        # Trace the midpoint
        trace = TracingTail(chord_group[1], time_traced=3, stroke_color=YELLOW)

        # 5. Animation
        self.play(ShowCreation(secant_line))
        self.play(ShowCreation(chord_group))
        self.add(trace)
        
        self.wait()
        
        # Rotate the line to show the locus
        self.play(
            angle_tracker.animate.set_value(PI),
            run_time=4,
            rate_func=linear
        )
        
        # Show the hidden circle
        self.play(ShowCreation(locus_circle))
        # locus_label = Text("Locus of midpoints", font_size=24, color=YELLOW).next_to(locus_circle, LEFT)
        # self.play(Write(locus_label))
        
        self.play(
            angle_tracker.animate.set_value(2*PI),
            run_time=4,
            rate_func=linear
        )
        self.wait(2)
