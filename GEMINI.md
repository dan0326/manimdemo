# Gemini Project Guidelines for manimdemo

This file helps me, Gemini, understand your project better and provide more tailored assistance. You can add notes here about your coding style, project goals, or common commands.

## Project Overview

This project uses the Manim library to create mathematical animations.

## How to Run Animations

To render and view an animation, use the following command structure. Remember to replace `your_script.py` and `YourSceneName` accordingly.

```bash
manimgl your_script.py YourSceneName
```

## Coding Conventions & Templates

This section is for code patterns you want me to follow.

### Template: Creating a Plane with a SurfaceMesh

When I need to draw a plane or other 3D surface, please create both a `ParametricSurface` for the surface itself and a `SurfaceMesh` for the wireframe. Then, group them together. This ensures consistency across the project.

**Template:**

```python
# 1. Define the Parametric Surface
surface_plane = ParametricSurface(
    lambda u, v: np.array([
        u,
        v,
        0  # Change this value for the plane's height (z-coordinate)
    ]),
    u_range=(-8, 8),
    v_range=(-8, 8),
    color=BLUE,
    opacity=0.8
)

# 2. Create the mesh for the surface
surface_mesh = SurfaceMesh(
    surface_plane,
    resolution=(30, 30),
    stroke_width=1.5,
    stroke_color=GREY_C
)

# 3. Group them for easier manipulation
surface_with_mesh = Group(surface_plane, surface_mesh)

# 4. Add the final group to the scene
self.add(surface_with_mesh)
```

**Key Points:**
- First, define the `ParametricSurface` with its mathematical function, range, color, and opacity.
- Second, create a `SurfaceMesh` that takes the `ParametricSurface` object as its first argument.
- Adjust `resolution`, `stroke_width`, and `stroke_color` for the mesh as needed.
- Finally, combine them in a `Group` before adding to the scene. This is the preferred pattern.

### Template: Filling Area Under a Curve

When you need to fill the area between a function's graph and the x-axis, use the following template. This is useful for visualizing integrals or highlighting specific regions.

**Template:**

```python
# 1. Define the function and the area object
def create_area():
    # Define your function f(x)
    func = lambda x: x**2  # Example: f(x) = x^2

    # Define the x-axis range for the filled area
    x_range = (-2, 2)  # Example: from x = -2 to x = 2

    # Create the area VMobject
    area = VMobject()
    area.set_points_as_corners([
        *[axes.c2p(x, 0) for x in np.linspace(x_range[0], x_range[1], 100)],
        *[axes.c2p(x, func(x)) for x in np.linspace(x_range[0], x_range[1], 100)][::-1]
    ])
    # Set the fill color and opacity
    area.set_fill(BLUE, opacity=0.5)
    # Remove the stroke
    area.set_stroke(width=0)
    return area

# 2. Create the area and add it to the scene
# Use always_redraw if the function is dynamic (e.g., depends on a ValueTracker)
area_to_fill = always_redraw(create_area)
self.add(area_to_fill)
```

**Key Points:**
- Define your mathematical `func` inside the `create_area` function.
- Specify the `x_range` (a tuple with start and end points) for the area you want to fill.
- The points for the `VMobject` are created by combining the points on the x-axis with the points on the function's curve.
- Use `always_redraw` if your function changes dynamically, otherwise a simple call to `create_area()` is sufficient.
- Customize the `set_fill` color and `opacity` as needed.