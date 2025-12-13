from manimlib import *

class GraphExample(Scene):
    def construct(self):
        axes= Axes((-3,10), (-1,8))
        axes.add_coordinate_labels()
        self.play(Write(axes, lag_ratio=0.01, run_time=1))

        #add sin graph N label
        sin_graph = axes.get_graph(
            lambda x: 2*math.sin(x),
            color=BLUE)
        sin_label = axes.get_graph_label(sin_graph, Tex("sin(x)"))

        #add relu graph N label
        relu_graph = axes.get_graph(
            lambda x : max(x, 0),
            use_smoothing=False,
            color=YELLOW)
        relu_label = axes.get_graph_label(relu_graph, Tex("ReLU"))

        #add step garph N label
        step_graph = axes.get_graph(
            lambda x: 2.0 if x >3 else 1.0,
            discontinuities=[3],
            color=GREEN)
        step_label = axes.get_graph_label(step_graph, Tex("step"))

        self.play(
            ShowCreation(sin_graph),
            FadeIn(sin_label, RIGHT)) #the RIGHT here still works!?

        self.wait(2)
        self.play(ReplacementTransform(sin_graph, relu_graph),
            FadeTransform(sin_label, relu_label))

        self.wait()
        self.play(ReplacementTransform(relu_graph, step_graph),
            FadeTransform(relu_label, step_label))

        #add a parabola
        parabola = axes.get_graph(lambda x : 0.25 * x**3)
        parabola.set_stroke(BLUE)
        self.play(
            FadeOut(step_graph),
            FadeOut(step_label),
            ShowCreation(parabola))
        self.wait()

        #add a dot on the parabola
        dot = Dot(color=RED)
        dot.move_to(axes.i2gp(2, parabola))
        self.play(FadeIn(dot, scale=-0.5))

        #animate dot on parabola
        x_tracker= ValueTracker(2)
        
        # Create tangent line
        tangent_line = always_redraw(
            lambda: axes.get_tangent_line(
                x_tracker.get_value(),
                parabola,
                length=5,
            )
        )
        
        f_always(
            dot.move_to,
            lambda: axes.i2gp(x_tracker.get_value(), parabola))
        
        # Add tangent line to the scene
        self.add(tangent_line)
        self.play(x_tracker.animate.set_value(4), run_time=3)
        self.play(x_tracker.animate.set_value(6), run_time=3)

