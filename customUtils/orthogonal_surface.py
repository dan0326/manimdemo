import numpy as np

def get_orthogonal_plane_func(normal: list, center: list):
    """Transform a parameterize plane function to gaurantee that it looks like a square in 3D space"""
    # 1. Normalize the normal vector
    n = np.array(normal) / np.linalg.norm(normal)
    
    # 2. Find a vector perpendicular to the normal (basis vector 1)
    # We pick a random vector and use cross product to find a perpendicular one
    if abs(n[0]) < 0.9: # Avoid singularity if normal is parallel to X
        basis_1 = np.cross(n, [1, 0, 0])
    else:
        basis_1 = np.cross(n, [0, 1, 0])
    basis_1 /= np.linalg.norm(basis_1)
    
    # 3. Find the third vector (basis vector 2) via cross product
    basis_2 = np.cross(n, basis_1)

    def plane_func(u, v):
        return center + u * basis_1 + v * basis_2
    
    # 4. Return the function
    return plane_func

def get_basis_vectors(normal: list):
    """takes in the normal vector of a plane and return its 2 basis vector"""
    # 1. Normalize the normal vector
    n = np.array(normal) / np.linalg.norm(normal)
    
    # 2. Find a vector perpendicular to the normal (basis vector 1)
    # We pick a random vector and use cross product to find a perpendicular one
    if abs(n[0]) < 0.9: # Avoid singularity if normal is parallel to X
        basis_1 = np.cross(n, [1, 0, 0])
    else:
        basis_1 = np.cross(n, [0, 1, 0])
    basis_1 /= np.linalg.norm(basis_1)
    
    # 3. Find the third vector (basis vector 2) via cross product
    basis_2 = np.cross(n, basis_1)

    return basis_1, basis_2