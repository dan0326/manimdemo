from manimlib_import_ext import *
from scipy.integrate import solve_ivp

def lorenz_system(t, state, sigma=10, rho=28, beta=8/3):
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]

#this gives points of the lorenz system at given time
def ode_solution_points(function, state0, time, dt=0.001):
    solution = solve_ivp(
        function,
        t_span=(0, time),
        y0=state0,
        t_eval=np.arange(0, time, dt)
    )
    return solution.y.T

class LorenzAttractor(InteractiveScene):
    def construct(self):
        # Set up the 3D axes
        axes = ThreeDAxes(
            x_range=(-50, 50, 5),
            y_range=(-50, 50, 5),
            z_range=(0, 50, 5),
            width=16,
            height=16,
            depth=8
        )
        axes.set_width(FRAME_WIDTH)
        axes.center()

        self.frame.reorient(48, 76, 1, (np.float32(0.0), np.float32(-0.0), np.float32(-1.02)), 10.00)
        self.add(axes)

        #add equations
        equations = Tex(R"""\begin{aligned}{\frac {\mathrm {d} x}{\mathrm {d} t}}&=\sigma (y-x) \\
            {\frac {\mathrm {d} y}{\mathrm {d} t}}&=x(\rho -z)-y \\
            {\frac {\mathrm {d} z}{\mathrm {d} t}}&=xy-\beta z 
            \end{aligned}""",
            t2c={
                "x" : RED,
                "y" : GREEN,
                "z" : BLUE
            },
            font_size=36)
        equations.fix_in_frame()
        equations.to_corner(UL)
        self.play(Write(equations))

        #Display Solutions
        epsilon = 0.001
        evolution_time = 15
        states = [[10, 10, 10+ n *epsilon] for n in range(3)]
        colors = color_gradient([BLUE, RED_E], len(states))
        curves = VGroup()
        for state, color in zip(states, colors):
            points = ode_solution_points(lorenz_system, state, evolution_time)
            curve=VMobject().set_points_as_corners(axes.c2p(*points.T))
            curve.set_stroke(color, 2)
            curves.add(curve)
        dots = Group(GlowDots(color= color) for color in colors)
        def update_dots(dots):
            for dot, curve in zip(dots, curves):
                dot.move_to(curve.get_end())
        dots.add_updater(update_dots)
        self.add(dots)
        self.play(*(
            ShowCreation(curve, run_time=evolution_time, rate_func=linear)
            for curve in curves
            ),
            self.frame.animate.reorient(170, 72, 0, (0, 0, -1), 10),
        run_time=evolution_time)

        