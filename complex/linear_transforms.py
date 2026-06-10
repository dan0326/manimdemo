from manimlib import *

def complex_func(z):
    return z**2

def get_complex_vector(plane, z, color=YELLOW):
    z_vect = Vector()
    z_vect.put_start_and_end_on(plane.n2p(0), plane.n2p(z))
    #z_vect.rotate(TAU/4, axis=z_vect.get_vector()) -> may be good for 3D vector
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

        #linear transform
        grid = NumberPlane((-25, 25), (-5, 5))
        matrix = [[1, 0.5], [0.25, 1]]
        linear_transform_words = VGroup(
            Text("This is what the matrix"),
            Matrix(matrix),
            Text("looks like")
        )
        linear_transform_words.arrange(RIGHT)
        linear_transform_words.to_edge(UP)
        linear_transform_words.set_stroke(WHITE, 3, behind=True, flat=True)
        self.play(ShowCreation(grid),
            FadeTransform(intro_words, linear_transform_words))
        self.wait()
        self.play(grid.animate.apply_matrix(matrix), run_time=3)
        self.wait(1)
        self.remove(grid, linear_transform_words)

        #set up complex map and axes
        c_grid = ComplexPlane()
        axes = Axes()
        moving_c_grid = c_grid.copy()
        c_grid.set_stroke(BLUE_E, 1)
        c_grid.add_coordinate_labels(font_size=24)
        self.play(Write(axes), Write(c_grid), run_time = 3)

        #transform vector and dot
        initial_complex_coord = 3 + 4j
        
        # Create original vector and dot on the original grid
        z_vect = get_complex_vector(c_grid, initial_complex_coord)
        z_dot = Dot(radius=0.05)
        z_dot.set_color(RED)
        z_dot.move_to(z_vect.get_end())
        
        # Prepare the moving grid for transformation
        moving_c_grid.prepare_for_nonlinear_transform()
        
        # Create moving versions that will transform with the grid
        moving_vector = get_complex_vector(moving_c_grid, initial_complex_coord, color=YELLOW)
        moving_dot = Dot(radius=0.05)
        moving_dot.set_color(RED)
        moving_dot.move_to(moving_vector.get_end())
        
        self.play(FadeIn(z_dot), FadeIn(z_vect))

        #animate scene
        self.play(
            FadeIn(z_dot),
            Write(c_grid, run_time=3),
            FadeIn(moving_c_grid))
        self.play(
            FadeIn(moving_dot),
            FadeIn(moving_vector))
        self.wait()
        
        #Apply the transformation
        self.frame.set_height(48)
        self.play(
            moving_c_grid.animate.apply_complex_function(complex_func),
            moving_vector.animate.apply_complex_function(complex_func),
            moving_dot.animate.apply_complex_function(complex_func),
            run_time=6)
        
        # After transformation, make sure dot stays at vector tip
        moving_dot.move_to(moving_vector.get_end())
        self.wait()