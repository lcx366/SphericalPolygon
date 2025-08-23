import numpy as np

from .math import spherical_to_cartesian

def polygon_perimeter(vertices): 
    '''
    Calculate the perimeter of a spherical polygon over a unit sphere.
    
    Usage: 
    perimeter = polygon_perimeter(vertices)

    Inputs:
    vertices -> [float 2d array] Vertices of a spherical polygon in format of [[lat_0,lon_0],..,[lat_n,lon_n]] with unit of degrees.
    Vertices can be arranged either counterclockwise or clockwise.
    
    Outputs:
    perimeter -> [float] Perimeter of the spherical polygon in radians. It is independent of how the vertices are arranged.

    Note: The spherical polygon has a latitude range of [-90,90] and a longitude range of [-180,180] or [0,360].
    '''
    lats,lons = vertices[:,0],vertices[:,1]

    N = len(vertices)
    polygon_xyz = spherical_to_cartesian(lons,lats,1)

    perimeter = 0
    for i in range(N-1):
        inner_prod = np.dot(polygon_xyz[i],polygon_xyz[i+1])
        # inner product for any two unit vectors should be in [-1,1] 
        if inner_prod > 1: inner_prod = 1
        if inner_prod < -1: inner_prod = -1
        perimeter += np.arccos(inner_prod)
    return perimeter    
