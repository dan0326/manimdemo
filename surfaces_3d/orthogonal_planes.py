from manimlib_import_ext import *

class OrthoSurface(InteractiveScene):
    def construct(self):

        
        # --- Inside your Scene class ---
        # The plane is z = 5 + x - y  =>  x - y - z = -5
        # The normal vector is (1, -1, -1)
        # A point on the plane (center) could be (0, 0, 5)

        # add axes
        axes = ThreeDAxes()
        axes.add_axis_labels()
        self.add(axes)
        
        # add the first plane 
        plane_func = get_orthogonal_plane_func(
            normal=[1, -1, -1], 
            center=[0, 0, 5]
        )
        planeh = ParametricSurface(
            plane_func,
            u_range=(-5, 5),
            v_range=(-5, 5),
            resolution=(30, 30),
            opacity=0.5
        )
        planeh.set_color_by_xyz_func("z")
        self.add(planeh)

        # add first line
        line1 = Line((0,0,5), (0,0,5) + 5 * get_basis_vectors([1, -1, -1])[1])
        line1.set_color(YELLOW)
        self.add(line1)

        # add the second plane
        self.frame.reorient(-5, 47, 0, (1.41, -1.06, 4.53), 6.23)
        new_normal = np.cross([1, -1, 0], get_basis_vectors([1, -1, -1])[0])
        new_func = get_orthogonal_plane_func(new_normal, [0,0,0])
        new_plane = ParametricSurface(
            new_func,
            u_range=(-1.5, 8.5),
            v_range=(-1.5, 8.5),
            resolution=(30, 30),
            opacity=0.5
        )
        self.add(new_plane)

        #add second line
        line2_vec = get_basis_vectors(new_normal)[1]
        line2 = Line((0,0,0) - 2* line2_vec, (0,0,0)+ 3* line2_vec)
        line2.set_color(RED)
        self.add(line2)
        self.frame.set_gamma(-30 * DEGREES)


