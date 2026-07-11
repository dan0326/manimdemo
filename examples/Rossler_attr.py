from manimlib_import_ext import *
from scipy.integrate import solve_ivp

def rossler_system(t, state, a=0.2, b=0.2, c=5.7):
    x, y, z = state
    
    dxdt = -y - z
    dydt = x + a * y
    dzdt = b + z * (x - c)
    return [dxdt, dydt, dzdt]

def ode_solution_points(function, state0, time, dt=0.001):
    result = solve_ivp(
        function,
        (0, time),
        state0,
        t_eval=np.arange(0, time, dt)
        )
    return result.y.T

class Rossler(InteractiveScene):
    def construct(self):
        #set up 3D axes
        axes = ThreeDAxes(
            x_range=(-50, 50, 5),
            y_range=(-50, 50, 5),
            z_range=(0, 50, 5),
            width=16,
            height=16,
            depth=8)
        axes.set_width(FRAME_WIDTH)
        axes.center()

        self.add(axes)
        self.frame.reorient(50, 73, 0, (1.31, -0.39, 0.01), 11.06)

        #add equations
        eqn = Tex(R"""\begin{cases}
            \dfrac{dx}{dt} = -y - z \\[1ex]
            \dfrac{dy}{dt} = x + ay \\[1ex]
            \dfrac{dz}{dt} = b + z(x - c)
            \end{cases}""",
            font_size=36)
        eqn.fix_in_frame()
        eqn.to_corner(UL)
        self.play(Write(eqn))

        #show solutions
        epsilon = 0.01
        evolution_time = 15
        states = [[10, 10, 10 + n*epsilon] for n in range(3)]
        colors = color_gradient((BLUE, YELLOW), len(states))
        curves = VGroup()
        for state, color in zip(states, colors):
            points = ode_solution_points(rossler_system, state, evolution_time)
            curve = VMobject().set_points_as_corners(axes.c2p(*points.T))
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
