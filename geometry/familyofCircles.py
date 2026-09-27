from manimlib import *
import numpy as np


class FamilyOfCircles(Scene):
    def construct(self):
        # Set up the coordinate plane
        plane = NumberPlane(
            x_range=(-5, 8, 1),
            y_range=(-4, 6, 1),
            width=8.6,
            height=6.6,
            background_line_style={
                "stroke_color": GREY_D,
                "stroke_width": 1,
                "stroke_opacity": 0.55,
            },
        )
        plane.shift(2.35 * LEFT + 0.25 * DOWN)
        plane.add_coordinate_labels(font_size=18)

        # Prepare the title and the equations in the side panel
        title = Text("A family of circles", font_size=42)
        title.to_corner(UR)

        general_equation = Tex(r"C+kL=0", font_size=52)
        circle_equation = Tex(
            r"C:\;x^2+y^2-4x-2y-4=0",
            font_size=28,
        )
        line_equation = Tex(
            r"L:\;x+y-1=0",
            font_size=28,
        )
        expanded_equation = Tex(
            r"x^2+y^2+(-4+k)x+(-2+k)y-(4+k)=0",
            font_size=25,
        )
        center_equation = Tex(
            r"O_k=\left(2-\frac{k}{2},\;1-\frac{k}{2}\right)",
            font_size=29,
        )
        radius_equation = Tex(
            r"r_k=\sqrt{\frac{k^2}{2}-2k+9}",
            font_size=29,
        )
        invariant_text = Text(
            "P and Q stay on every circle",
            font_size=25,
            color=RED,
        )

        k_tracker = ValueTracker(0)
        k_number = DecimalNumber(
            0,
            num_decimal_places=2,
            include_sign=True,
            font_size=38,
            color=GREEN,
        )
        k_number.add_updater(
            lambda number: number.set_value(k_tracker.get_value())
        )
        k_readout = VGroup(Tex("k=", font_size=38), k_number)
        k_readout.arrange(RIGHT, buff=0.12)

        panel = VGroup(
            general_equation,
            circle_equation,
            line_equation,
            expanded_equation,
            k_readout,
            center_equation,
            radius_equation,
            invariant_text,
        )
        panel.arrange(DOWN, buff=0.31)
        panel.set_width(4.35)
        panel.next_to(title, DOWN, buff=0.28)
        panel.align_to(title, RIGHT)
        panel_background = BackgroundRectangle(
            panel,
            color=BLACK,
            fill_opacity=0.82,
            buff=0.22,
        )

        # Introduce the family of circles with its general equation
        self.play(
            FadeIn(title, DOWN),
            FadeIn(panel_background),
            Write(general_equation),
        )

        # Draw the original circle on the coordinate plane
        base_circle = self.get_circle(plane, 0, BLUE, stroke_width=4)
        circle_label = Tex("C", color=BLUE, font_size=32)
        circle_label.move_to(plane.c2p(4.45, 3.25))

        self.play(
            ShowCreation(plane, lag_ratio=0.02),
            ShowCreation(base_circle),
            FadeIn(circle_label),
            run_time=2,
        )

        # Draw the radical axis and show the two defining equations
        radical_axis = Line(
            plane.c2p(-5, 6),
            plane.c2p(5, -4),
            color=YELLOW,
            stroke_width=4,
        )
        line_label = Tex("L", color=YELLOW, font_size=32)
        line_label.move_to(plane.c2p(4.4, -3.65))

        self.play(
            ShowCreation(radical_axis),
            FadeIn(line_label),
            Write(circle_equation),
            Write(line_equation),
        )

        # Mark the two fixed points shared by every circle in the family
        root = np.sqrt(14) / 2
        point_p = plane.c2p(1 + root, -root)
        point_q = plane.c2p(1 - root, root)
        common_dots = VGroup(
            Dot(point_p, color=RED, radius=0.07),
            Dot(point_q, color=RED, radius=0.07),
        )
        common_labels = VGroup(
            Tex("P", color=RED, font_size=28).next_to(
                point_p, DOWN + RIGHT, buff=0.08
            ),
            Tex("Q", color=RED, font_size=28).next_to(
                point_q, UP + LEFT, buff=0.08
            ),
        )

        self.play(
            FadeIn(common_dots, scale=0.5),
            Write(common_labels),
            FadeIn(invariant_text, UP),
        )
        self.wait()

        # Expand C + kL and display the live value of k
        self.play(
            Write(expanded_equation),
            FadeIn(k_readout),
        )

        # Build the moving circle, its center, and the center's locus
        family_circle = always_redraw(
            lambda: self.get_circle(
                plane,
                k_tracker.get_value(),
                GREEN,
                stroke_width=5,
            )
        )
        center_dot = always_redraw(
            lambda: Dot(
                plane.c2p(*self.get_center(k_tracker.get_value())),
                color=ORANGE,
                radius=0.055,
            )
        )
        center_locus = DashedLine(
            plane.c2p(-3, -4),
            plane.c2p(7, 6),
            color=ORANGE,
            stroke_width=2,
        )

        self.play(
            base_circle.animate.set_stroke(opacity=0.22),
            FadeIn(family_circle),
            ShowCreation(center_locus),
            FadeIn(center_dot),
            Write(center_equation),
            Write(radius_equation),
        )

        # Move through several values of k and leave faint circle snapshots
        snapshots = VGroup()
        for k_value in (-2, 1.5, 4, -1, 3):
            self.play(
                k_tracker.animate.set_value(k_value),
                run_time=1.7,
                rate_func=smooth,
            )
            snapshot = self.get_circle(
                plane,
                k_value,
                GREEN,
                stroke_width=2,
            )
            snapshot.set_stroke(opacity=0.22)
            snapshots.add(snapshot)
            self.add(
                snapshot,
                family_circle,
                center_dot,
                common_dots,
                common_labels,
            )

        # Sweep across the family once more, then return to the original circle
        self.play(
            k_tracker.animate.set_value(-2),
            run_time=1.5,
            rate_func=smooth,
        )
        self.play(
            k_tracker.animate.set_value(4),
            run_time=5,
            rate_func=linear,
        )
        self.play(
            k_tracker.animate.set_value(0),
            run_time=2,
            rate_func=smooth,
        )
        self.wait(2)

    @staticmethod
    def get_center(k_value):
        return 2 - k_value / 2, 1 - k_value / 2

    @classmethod
    def get_circle(cls, plane, k_value, color, stroke_width):
        center_x, center_y = cls.get_center(k_value)
        radius = np.sqrt(k_value**2 / 2 - 2 * k_value + 9)
        scene_radius = np.linalg.norm(
            plane.c2p(radius, 0) - plane.c2p(0, 0)
        )
        circle = Circle(
            radius=scene_radius,
            color=color,
            stroke_width=stroke_width,
        )
        circle.move_to(plane.c2p(center_x, center_y))
        return circle
