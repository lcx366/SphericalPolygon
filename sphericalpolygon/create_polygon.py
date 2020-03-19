import numpy as np
from .polygonclasses.sphericalpolygon import Sphericalpolygon

def create_polygon(vertices):
    '''
    Create an instance of class Sphericalpolygon.
    
    Usage:
    polygon = create_polygon(vertices)

    Inputs:
    vertices -> [float 2d array] Vertices that make up the polygon in form of [[lat_0,lon_0],...,[lat_n,lon_n]] with unit of degrees. 
    If the first vertex is not equal to the last one, a point is automatically added to the end of the vertices sequence to form a closed polygon. 
    Vertices can be arranged either counterclockwise or clockwise.

    Outputs:
    polygon -> an instance of class Sphericalpolygon 

    Note: The spherical polygon has a latitude range of [-90°,90°] and a longitude range of [-180°,180°] or [0°,360°].
    '''
    
    if (vertices[0] != vertices[-1]).all():
        vertices = np.append(vertices,[vertices[0]],axis=0) # create a closed spherical polygon

    return Sphericalpolygon(vertices)