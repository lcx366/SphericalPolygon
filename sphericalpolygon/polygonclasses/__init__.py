'''
sphericalpolygon polygonclasses subpackage

This subpackage defines some classes that facilitate the processing of the spherical polygons.

Class structure:

    Sphericalpolygon

        - attributes:
            - polygon: vertices of a closed spherical polygon in form of [[lat_0,lon_0],...,[lat_n,lon_n]]
            - lats: latitudes of the spherical polygon in degrees
            - lons: longitudes of the spherical polygon in degrees
            - arrangement: vertex arrangement; it can be counterclockwise or clockwise

            - methods:
            - contains_points: determine if a single point or multiple points are inside the spherical polygon.
            - area: calculate the area of the spherical polygon.
            - inertia: calculate the inertia tensor of the spherical polygon.
'''