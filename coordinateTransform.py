from manimlib import *

class OpeningManimExample(Scene):
    def construct(self):
        #add words
        intro_words = Text("""
            The original motivation for manim was to
            better illustrate mathematical functions
            as transformations.
            """)
        intro_words.to_edge(UP)
        self.play(Write(intro_words))
        self.wait(2)
        self.remove(intro_words)

        #linear tranasform
        grid = NumberPlane((-10, 10), (-5, 5))
        matrix = [[1, 1], [0, 1]]
        self.play(ShowCreation(grid))
        self.wait()
        self.play(grid.animate.apply_matrix(matrix), run_time=3)
        self.wait()

        #complex map
        c_grid = ComplexPlane()
        moving_c_grid = c_grid.copy()
        moving_c_grid.prepare_for_nonlinear_transform()
        c_grid.set_stroke(BLUE_E, 1)
        c_grid.add_coordinate_labels(font_size=24)
        self.play(
            FadeOut(grid),
            Write(c_grid, run_time=3),
            FadeIn(moving_c_grid))
        self.wait()
        self.play(moving_c_grid.animate.apply_complex_function(lambda z: z**2),
            run_time=6)
        self.wait()