from math import sqrt
from manimlib_import_ext import *

class DemoScene(InteractiveScene):
    def construct(self):
        square = Square()
        square.set_fill(BLUE, 0.5)
        square.set_stroke(WHITE, 1)

        grid = square.get_grid(10, 10, buff=0.5)
        grid.set_height(7)

        labels = index_labels(grid)

        self.add(labels)
        self.add(grid)

        #animations
        def flip(square):
            if square.get_fill_color() == BLUE:
                target_color = GREY_C
            else:
                target_color = BLUE
            return square.animate.set_color(target_color).flip(RIGHT)

        for n in range(2, 10):
            highlight = grid[::n].copy()
            highlight.set_stroke(YELLOW, width=2)
            highlight.set_fill(opacity=0)
            self.play(
                ShowCreation(highlight, lag_ratio=0.05),
                run_time = 2 / math.sqrt(n))
            self.play(
                LaggedStartMap(flip, grid[::n],lag_ratio=0.05),
                FadeOut(highlight),
                run_time = 2 / math.sqrt(n))