from manimlib import *

class GraphExample(Scene):
    def construct(self):
        axes= Axes((-3,10), (-1,8))
        axes.add_coordinate_labels()
        self.play(Write(axes, lag_ratio=0.01, run_time=1))

        #add sin graph
        sin_graph = axes.get_graph(
            lambda x: 2*math.sin(x),
            color=BLUE)

        #add relu graph
        relu_graph = axes.get_graph(
            lambda x : max(x, 0),
            use_smoothing=False,
            color=YELLOW)

        #add step garph
        step_graph = axes.get_graph(
            lambda x: 2.0 if x >3 else 1.0,
            discontinuities=[3],
            color=GREEN)

        #add labels to graph
        sin_label = axes.get_graph_label(sin_graph, Text("sin(x)"))

