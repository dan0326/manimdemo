from manimlib import *

def complex_func(z):
    return z**2

def get_complex_vector(plane, z, color=YELLOW):
    z_vect = Vector()
    z_vect.put_start_and_end_on(plane.n2p(0), plane.n2p(z))
    #z_vect.rotate(TAU/4, axis=z_vect.get_vector())
    z_vect.set_color(color)
    return z_vect

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
        grid = NumberPlane((-25, 25), (-5, 5))
        matrix = [[1, 1], [0, 1]]
        self.play(ShowCreation(grid))
        self.wait()
        self.play(grid.animate.apply_matrix(matrix), run_time=3)
        self.wait()

        #complex map
        self.remove(grid)
        initail_complex_coord = 3 +4j
        self.camera.frame.set_height(25)
        c_grid = ComplexPlane((-25, 25), (-25, 25))
        z_vect = get_complex_vector(c_grid, initail_complex_coord)
        z_dot = Dot(radius=0.5)
        z_dot.set_color(RED)
        z_dot.f_always.move_to(lambda: z_vect.get_end())
        self.add(z_dot)
        moving_c_grid = c_grid.copy()
        moving_c_grid.prepare_for_nonlinear_transform()
        moving_vector = z_vect.copy()
        moving_dot = z_dot.copy()
        moving_dot.f_always.move_to(lambda: moving_vector.get_end())
        c_grid.set_stroke(BLUE_E, 1)
        c_grid.add_coordinate_labels(font_size=24)
        self.play(
            Write(c_grid, run_time=3),
            FadeIn(moving_c_grid),
            FadeOut(c_grid))
        self.wait()
        transformed_complex_coord = complex_func(initail_complex_coord)
        new_position = c_grid.c2p(transformed_complex_coord.real, transformed_complex_coord.imag)
        self.play(moving_c_grid.animate.apply_complex_function(complex_func),
            moving_vector.animate.apply_complex_function(complex_func),
            moving_dot.animate.apply_complex_function(complex_func),
            run_time=6)
        self.wait()