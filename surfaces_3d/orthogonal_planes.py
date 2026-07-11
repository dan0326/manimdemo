from numpy import arccos
from manimlib_import_ext import *

def get_skew_distance(p1, v1, p2, v2):
    point_vec = np.array(p2) - np.array(p1)
    cross_prod = np.cross(v1, v2)
    if np.allclose(cross_prod, 0):
        project = (np.dot(point_vec, v1) / np.dot(v1, v1)) * v1
        distance = np.linalg.norm(point_vec - project)
    else:
        connecting_vec = np.cross(v1, v2)
        distance = abs(np.dot(connecting_vec, point_vec) / np.linalg.norm(connecting_vec))
    return distance

class OrthoSurface(InteractiveScene):
    def construct(self):

        # --- Inside your Scene class ---
        # The plane is z = 5 + x - y  =>  x - y - z = -5
        # The normal vector is (1, -1, -1)
        # A point on the plane (center) could be (0, 0, 5)

        #add equations
        equations = Tex(R"""P_1: x-y-z=5\\
                            P_2: x+y+z=0""",
            font_size=36)
        equations.fix_in_frame()
        equations.to_corner(UL)
        self.play(Write(equations), run_time = 1)
        
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
        line1_vec = get_basis_vectors([1, -1, -1])[1]
        line1 = Line((0,0,5), (0,0,5) + 5 * line1_vec)
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

        # shift line2 and move camera further
        normal_vec = get_basis_vectors(new_normal)[0] / np.linalg.norm(get_basis_vectors(new_normal)[0])
        d = get_skew_distance((0, 0, 5), line1_vec, (0,0,0), line2_vec)
        line2_start_pos = line2.copy()
        self.add(line2_start_pos)
        self.play((line2.animate.shift(d * normal_vec)),
            self.frame.animate.reorient(-6, 49, -30, (1.77, -1.46, 4.14), 8.62), run_time = 2)
        

        # rotate line2 vector to cross with line1
        dot_prod = np.dot(line1_vec, line2_vec)
        rotate_angle = arccos(dot_prod / (np.linalg.norm(line1_vec) * np.linalg.norm(line2_vec)))
        point_rotate_about = (0,0,0) + 3 * line2_vec + d * get_basis_vectors(new_normal)[0] / np.linalg.norm(get_basis_vectors(new_normal)[0])
        self.play(line2.animate.rotate(rotate_angle, get_basis_vectors(new_normal)[0], point_rotate_about), run_time= 1.5)
        normal_arrow = Arrow(point_rotate_about, point_rotate_about+ normal_vec*2)
        normal_arrow.rotate(TAU/4, normal_vec)
        normal_arrow.set_color(BLUE)
        self.play(GrowArrow(normal_arrow), FadeOut(line2))

        

