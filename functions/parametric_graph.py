from manimlib import *

def show_dot()

class paramGraph(InteractiveScene):
    def construct(self):

        #add axes
        xyspan = 5
        axes = Axes((-4, 6), (-4, 5), unit_size=0.8)
        axes.add_coordinate_labels()
        self.add(axes)

        #add lines
        line_h = Line(axes.c2p(-xyspan, -2), axes.c2p(7, -2), color=BLUE)
        line_h.set_stroke(width=1.25)
        line_v = Line(axes.c2p(1, -5), axes.c2p(1, 5), color=RED)
        line_v.set_stroke(width=1.25)
        self.add(line_h)
        self.add(line_v)

        #add function
        main_line = Line(axes.c2p(6, -2), axes.c2p(-3, 4))
        main_line.set_stroke(width=1.25)
        self.add(main_line)
