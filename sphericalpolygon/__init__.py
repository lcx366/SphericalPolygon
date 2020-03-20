'''
sphericalpolygon package

This package is an archive of scientific routines for spherical polygons.   
Currently, operations on spherical polygons include:
    1. calculate the area or mass(if the area density is given) 
    2. calculate the perimeter
    3. identify the location of the centroid 
    4. compute the geometrical or physical moment of inertia tensor
    5. determine whether one or more points are inside the spherical polygon.
'''

from .create_polygon import create_polygon
