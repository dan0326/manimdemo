from manimlib import *

class ceecParabola(Scene):
    def construct(self):
        xyspan = 5
        axes = Axes((-xyspan, xyspan), (-xyspan, xyspan))
        axes.add_coordinate_labels()
        self.add(axes)

        #add parabola
        a = ValueTracker(-0.5)
        parabola = always_redraw(
            lambda: FunctionGraph(
                lambda x: 3 * a.get_value() * x**2 + 1 - a.get_value(),
                color=BLUE
            )
        )
        self.add(parabola)

        #add integral sign
        equation = Tex(R"""\int_{-1}^{1}{3a}x^{2}+\left(1-a\right)""",
            font_size=36,
            t2c={
                "a": RED
            })
        equation.fix_in_frame();
        equation.to_corner(UL);
        self.add(equation);

        #add area
        def create_area():
            func = lambda x: 3 * a.get_value() * x**2 + 1 - a.get_value()
            area = VMobject()
            area.set_points_as_corners([
                *[axes.c2p(x, 0) for x in np.linspace(-1, 1, 100)],
                *[axes.c2p(x, func(x)) for x in np.linspace(-1, 1, 100)][::-1]
            ])
            area.set_fill(YELLOW, opacity=0.5)
            area.set_stroke(width=0)
            return area
        area = always_redraw(create_area)
        self.add(area)

        #add a value display
        a_label = always_redraw(
            lambda: VGroup(
            Tex("a = ", font_size=36),
                DecimalNumber(a.get_value(), num_decimal_places=2, font_size=32)
            ).arrange(RIGHT).next_to(equation, DOWN)
        )
        self.add(a_label)

        #add [-1, 1] line for reference
        lineat1 = Line(axes.c2p(1, -4), axes.c2p(1, 4), color=RED)
        self.add(lineat1)
        lineat_1 = Line(axes.c2p(-1, -4), axes.c2p(-1, 4), color=RED)
        self.add(lineat_1)

        #add intersecting point with x-axis
        def create_intersections():
            a_val = a.get_value()
            dots = VGroup()
            if a_val != 0:
                discriminant= (a_val-1)/(3*a_val)
                if discriminant>0:
                    x1=np.sqrt(discriminant)
                    x2=-np.sqrt(discriminant)
                    dot1 = Dot(axes.c2p(x1, 0), radius=0.075)
                    dot1.set_color(GREEN)
                    dot2 = Dot(axes.c2p(x2, 0), radius=0.075)
                    dot2.set_color(GREEN)
                    dots.add(dot1, dot2)
                elif discriminant == 0:  # One solution (touches x-axis)
                    dot = Dot(axes.c2p(0, 0), radius=0.075)
                    dot.set_color(RED)
                    dots.add(dot)
            return dots
        intersections = always_redraw(create_intersections)
        self.add(intersections)

        #animate all
        a.set_value(-0.5)
        self.play(a.animate.set_value(0), run_time=6)
        self.wait(1)
        self.play(a.animate.set_value(1), run_time=4)

