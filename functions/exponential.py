from manimlib_import_ext import *

class TheExponential(InteractiveScene):
    def construct(self):
        # Set up input and output space, top an bottom
        in_line = NumberLine((-5, 5), unit_size=1.5)
        in_line.move_to(2 * UP)
        in_line.add_numbers(font_size=20)

        out_line = NumberLine((-21, 21), unit_size=1.5)
        out_line.move_to(2 * DOWN)
        out_line.add_numbers(font_size=20)

        arrow_buff = 0.75
        func_arrow = Arrow(in_line.n2p(0), out_line.n2p(1), buff=arrow_buff, thickness=6)
        func_label = Tex(R"e^{x}", font_size=72)
        func_label.next_to(func_arrow.get_center(), UR, buff=MED_SMALL_BUFF)
        og_func_arrow = func_arrow.copy()

        self.add(in_line, out_line)

        # Show example dots
        sample_xs = np.arange(-4, 4.25, 0.25)
        in_dots = Group(*[TrueDot(in_line.n2p(x)) for x in sample_xs])
        out_dots = Group(*[TrueDot(out_line.n2p(np.exp(x))) for x in sample_xs])
        all_dots = Group(in_dots, out_dots)
        for dots in all_dots:
            for dot in dots:
                dot.set_radius(0.1)
                dot.make_3d()
                dot.deactivate_depth_test()
                dot.set_glow_factor(0.15)
            dots.set_submobject_colors_by_gradient(YELLOW, BLUE, interp_by_hsl=True)

        self.play(LaggedStartMap(FadeIn, in_dots, lag_ratio=0.1, run_time=1))
        self.play(
            GrowArrow(func_arrow),
            FadeIn(func_label, 0.25 * func_arrow.get_vector()),
            TransformFromCopy(in_dots, out_dots, lag_ratio=0.01, run_time=2),
        )
        self.wait()