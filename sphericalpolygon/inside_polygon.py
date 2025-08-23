import numpy as np

from .math import Rot,spherical_to_cartesian,cartesian_to_spherical,matrix_dot_vector_broadcast

def inside_polygon(
        points: np.ndarray,
        vertices: np.ndarray,
        arrangement: str,
        tolerance: float = 0.1
) -> np.ndarray:
    """
    Determines if points are inside spherical polygons using the angle summation method.

    This function is fully vectorized to handle multiple points and a single polygon
    efficiently. The core principle is that for a point inside a polygon, the sum
    of the angles subtended by the polygon's edges at that point will be ±2π.

    Inputs:
        points -> [np.ndarray] An array of points to check, with shape (N, 2). Each row is [latitude, longitude] in degrees.
        vertices -> [np.ndarray] An array of polygon vertices, with shape (M, 2). Each row is [latitude, longitude] in degrees.
        arrangement -> [str] The winding order of the polygon vertices. Must be either 'Counterclockwise' or 'Clockwise'.
        tolerance -> [float, optional, default=0.1] The numerical tolerance for checking if the sum of angles equals ±2π.

    Returns:
        flags -> [np.ndarray] A boolean array of shape (N,), where `True` indicates the corresponding point is inside the polygon.

    Note:
        The input `vertices` need to be explicitly closed; i.e., the last vertex should be the same as the first.

    Raises:
        ValueError: If the `arrangement` string is not one of the valid options.
    """

    # Ensure inputs are NumPy arrays for vectorized operations.
    points = np.asarray(points)

    # Extract latitude and longitude for clarity. Note: The algorithm uses
    # longitude first, then latitude, consistent with mathematical conventions.
    point_lons, point_lats = points[:, 1], points[:, 0]
    vertex_lons, vertex_lats = vertices[:, 1], vertices[:, 0]

    # Coordinate System Transformation
    # The core of the algorithm: rotate the celestial sphere so that each test
    # point moves to the North Pole (lat=90). In this new coordinate system,
    # the change in longitude of the transformed polygon vertices directly
    # corresponds to the angle subtended by each edge.

    # Calculate the rotation matrix for each point to move it to the North Pole.
    # `Rot` expects [lon, colatitude]. Colatitude = 90 - latitude.
    # This results in a stack of rotation matrices, one for each point.
    rotation_matrices = Rot('ZY', np.stack([point_lons, 90 - point_lats], axis=1))

    # Convert polygon vertices from spherical (lon, lat) to 3D Cartesian coordinates.
    polygon_cartesian = spherical_to_cartesian(vertex_lons, vertex_lats, 1)

    # Apply each rotation matrix to the set of polygon vertices.
    # This uses a broadcasted matrix-vector product.
    # Input: (N, 3, 3) matrices, (M+1, 3) vectors
    # Output: (N, M+1, 3) transformed vertices, where N is number of points.
    polygon_cartesian_transformed = matrix_dot_vector_broadcast(rotation_matrices, polygon_cartesian)

    # Angle Summation in the Transformed Frame
    # Convert the transformed Cartesian vertices back to spherical coordinates.
    # We need the longitudes in radians for angle calculations.
    polygon_spherical_transformed = cartesian_to_spherical(
        polygon_cartesian_transformed[..., 0],
        polygon_cartesian_transformed[..., 1],
        polygon_cartesian_transformed[..., 2],
        degrees=False
    )
    # Extract the longitudes of the transformed polygon vertices. Shape: (N, M+1)
    lons_transformed = polygon_spherical_transformed[..., 0]

    # Calculate the angular difference (change in longitude) for each polygon edge.
    # This is the angle subtended by each edge at the new North Pole (our test point).
    d_lons = lons_transformed[:, 1:] - lons_transformed[:, :-1]

    # Correct for the longitude wrap-around (e.g., from +179 deg to -179 deg).
    # This maps all angular differences to the shortest path in [-π, π].
    d_lons_corrected = (d_lons + np.pi) % (2 * np.pi) - np.pi

    # Sum the angles for each point. The result is a 1D array of total angles.
    sum_of_angles = np.sum(d_lons_corrected, axis=1)

    # Final Determination
    # Check if the sum of angles is close to ±2π, which indicates the point is inside.
    if arrangement == 'Counterclockwise':
        # For a counter-clockwise polygon, the sum should be +2π.
        flags = np.isclose(sum_of_angles, 2 * np.pi, atol=tolerance)
    elif arrangement == 'Clockwise':
        # For a clockwise polygon, the sum should be -2π.
        flags = np.isclose(sum_of_angles, -2 * np.pi, atol=tolerance)
    else:
        raise ValueError("Arrangement must be either 'Counterclockwise' or 'Clockwise'.")

    return flags
