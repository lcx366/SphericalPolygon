import numpy as np
from scipy.spatial.transform import Rotation

TWOPI = 2 * np.pi

def matrix_dot_vector_unicersal(matrix, vector):
    """
    Computes the dot product of matrices and vectors.

    This function correctly handles:
    1. Element-wise operations on matching batch dimensions:
       e.g., (8, 18, 3, 3) @ (8, 18, 3) -> (8, 18, 3)
    2. Applying one matrix to many vectors:
       e.g., (3, 3) @ (10, 3) -> (10, 3)
    3. Applying many matrices to one vector (requires broadcasting):
       e.g., (5, 3, 3) @ (3,) -> (5, 3)

    Inputs:
        matrix -> [array-like] Multi-dimensional matrix.
        vector -> [array-like] Multi-dimensional vector.

    Outputs:
        vector_trans -> [array-like] Transformed vectors.
    """
    vector = np.asarray(vector)
    return np.matmul(matrix, vector[..., None]).squeeze(-1)

def matrix_dot_vector_broadcast(matrix, vector):
    """
    Computes the broadcasted dot product of a batch of matrices and a set of vectors.

    This function handles a common broadcasting scenario where each matrix in a batch
    is applied to every vector in a given set. It effectively computes the
    matrix-vector product over the Cartesian product of the two inputs.

    The core of this function is the Einstein summation convention string 'bij,nj->bni'.

    Usage:
        >>> matrices = np.random.rand(5, 3, 3)
        >>> vectors = np.random.rand(4, 3)
        >>> vector_trans = matrix_dot_vector_broadcast(matrices, vectors)
        >>> vector_trans.shape # shape (5, 4, 3)

    Inputs:
        matrix -> [array-like] Multi-dimensional matrix.
        vector -> [array-like] Multi-dimensional vector.

    Outputs:
        vector_trans -> [array-like] Transformed vectors.
    """
    return np.einsum('bij,nj->bni', matrix, vector)

def spherical_to_cartesian(ra, dec, r, degrees=True):
    """
    Convert spherical coordinates (Right Ascension, Declination, Range) to Cartesian coordinates.

    Usage:
        >>> spherical_to_cartesian(45, 45, 1)
        array([0.5      , 0.5      , 0.70710678])
        >>> spherical_to_cartesian([45, 90], [45, 45], [1, 1])
        array([[5.00000000e-01, 5.00000000e-01, 7.07106781e-01],
               [3.74939946e-33, 7.07106781e-01, 7.07106781e-01]])
    Inputs:
        ra -> [array-like] Right Ascension.
        dec -> [array-like] Declination.
        r -> [array-like] Distance.
        degrees -> [bool, optional, default=True] Specifies if RA and Dec are in degrees or radians.
    Outputs:
        xyz -> [array-like] Cartesian coordinates as an array of shape (3,) or (N, 3).
    """
    if degrees:
        ra = np.radians(ra)
        dec = np.radians(dec)

    x = r * np.cos(dec) * np.cos(ra)
    y = r * np.cos(dec) * np.sin(ra)
    z = r * np.sin(dec)

    return np.stack([x, y, z], axis=-1)


def cartesian_to_spherical(x, y, z, degrees=True):
    """
    Convert Cartesian coordinates to spherical coordinates (Right Ascension, Declination, Distance).

    Usage:
        >>> cartesian_to_spherical(0.5, 0.5, 0.70710678)
        array([ 45.,  45.,   1.])
        >>> cartesian_to_spherical([0.5, 0], [0.5, 0], [0.70710678, 1])
        array([[ 45.,  45.,   1.],
               [  0.,  90.,   1.]])
    Inputs:
        x -> [float or array-like] X coordinate.
        y -> [float or array-like] Y coordinate.
        z -> [float or array-like] Z coordinate.
        degrees -> [bool, optional, default=True] Specifies if RA and Dec should be returned in degrees or radians.
    Outputs:
        ra_dec_r -> [array-like] Spherical coordinates as an array of shape (3,) or (N, 3).
    """
    r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
    ra = np.arctan2(y, x) % TWOPI # normalize RA to [0, 2pi)
    dec = np.arcsin(z / r)

    if degrees:
        ra = np.degrees(ra)
        dec = np.degrees(dec)

    return np.stack([ra, dec, r], axis=-1)


def Rot(seq, angles, degrees=True):
    """
    Rotate a reference frame around a sequence of axes.
    Note: The Rot is noly suitable for a right-handed reference frame !!

    Usage:
        >>> seq = 'XY'
        >>> angles = [60,30]
        >>> rotation_matrix = Rot(seq,angles)
    Inputs:
        seq -> [str] Sequence of axes for rotation, such as 'Z' or 'XY'.
        angles -> [float,list of float] Rotation angles in [rad] or [deg]
        degrees -> [bool,optional,default=True] If True, the rotation angles are assumed to be in degrees
    Outputs:
        rotation_matrix -> [2D array of 3x3] Rotation matrix from the source reference frame to target reference frame
    """
    if np.isscalar(angles):
        rotation_matrix = Rotation.from_euler(seq, angles, degrees).as_matrix().T
    else:
        angles = np.array(angles)
        if len(seq) > 1:
            if angles.ndim == 1:
                rotation_matrix = Rotation.from_euler(seq, angles, degrees).as_matrix().T
            elif angles.ndim == 2:
                rotation_matrix = Rotation.from_euler(seq, angles, degrees).as_matrix().transpose(0, 2, 1)
        else:
            rotation_matrix = Rotation.from_euler(seq, angles, degrees).as_matrix().transpose(0, 2, 1)

    return rotation_matrix
