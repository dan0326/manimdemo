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

```python
#this is used to mark a area up, so we can draw color inside...
def create_area():
            func = lambda x: 3 * a.get_value() * x**2 + 1 - a.get_value() #this is the desired function, a is a valuretracker
            area = VMobject()
            area.set_points_as_corners([
                *[axes.c2p(x, 0) for x in np.linspace(-1, 1, 100)],
                *[axes.c2p(x, func(x)) for x in np.linspace(-1, 1, 100)][::-1]
            ])
            area.set_fill(YELLOW, opacity=0.5)
            area.set_stroke(width=0)
            return area
        area = always_redraw(create_area)
        self.add(area)