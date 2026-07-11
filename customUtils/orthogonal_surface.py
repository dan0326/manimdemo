import numpy as np
from typing import Callable, Tuple
from numpy.typing import ArrayLike

def get_basis_vectors(normal: ArrayLike) -> Tuple[np.ndarray, np.ndarray]:
    """Takes in the normal vector of a plane and returns its 2 basis vectors."""
    # Ensure input is a numpy array for vector math
    n = np.array(normal, dtype=float)
    n /= np.linalg.norm(n)
    
    # Avoid singularity if normal is parallel to X
    if abs(n[0]) < 0.9:
        basis_1 = np.cross(n, [1, 0, 0])
    else:
        basis_1 = np.cross(n, [0, 1, 0])
        
    basis_1 /= np.linalg.norm(basis_1)
    basis_2 = np.cross(n, basis_1)

    return basis_1, basis_2

def get_orthogonal_plane_func(
    normal: ArrayLike, 
    center: ArrayLike
) -> Callable[[float, float], np.ndarray]:
    """Returns a parameterized function for a square-looking plane in 3D space."""
    
    basis_1, basis_2 = get_basis_vectors(normal)
    c = np.array(center, dtype=float)

    def plane_func(u: float, v: float) -> np.ndarray:
        return c + u * basis_1 + v * basis_2
    
    return plane_func
