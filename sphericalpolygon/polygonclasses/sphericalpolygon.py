import numpy as np
from ..inside_polygon import inside_polygon
from ..excess_area import polygon_excess,polygon_area
from ..inertia import polygon_inertia

class Sphericalpolygon(object):
    '''
    class Sphericalpolygon

    - attributes:
        - polygon: vertices of a closed spherical polygon in form of [[lat_0,lon_0],...,[lat_n,lon_n]]
        - lats: latitudes of the spherical polygon in degrees
        - lons: longitudes of the spherical polygon in degrees
        - arrangement: vertex arrangement; it can be counterclockwise or clockwise

    - methods:
        - contains_points: determine if a single point or multiple points are inside the spherical polygon.
        - area: calculate the area or mass of the spherical polygon.
        - inertia: calculate the geometrial or physical moment of inertia tensor of the spherical polygon.
    '''

    def __init__(self,polygon):

        self.polygon = polygon
        self.lats = polygon[:,0]
        self.lons = polygon[:,1]

        excess = polygon_excess(polygon)
        if 0 < excess < 2*np.pi or excess < -2*np.pi: flag = 'Counterclockwise'
        if -2*np.pi < excess < 0 or excess > 2*np.pi: flag = 'Clockwise'

        self.arrangement = flag


    def __repr__(self):
    
        return 'instance of class Sphericalpolygon'

    def contains_points(self,points):
        '''
        Determine if a single point or multiple points are inside the given spherical polygon.

        Usage: 
        flag = polygon.contains_points([30,102])
        flags = polygon.contains_points([[30,102],[-75,33]])

        Inputs:
        points -> [float array with 2 elements or float 2d array] single point or multiple points to be determined in form of [lat,lon] or [[lat_0,lon_0],..,[lat_n,lon_n]] with unit of degrees.

        Outputs:
        flags -> [bool or bool array] If True, the point is inside the polygon, otherwise, it is outside.
        '''
        polygon = self.polygon
        arrangement = self.arrangement
        if np.ndim(points) == 1:
            return inside_polygon(points,polygon,arrangement)
        else:
            flags = []
            for point in points:
                flag = inside_polygon(point,polygon,arrangement)
                flags.append(flag)
            np.array(flags)
            return flags   	

    def area(self, R = 1,rho = 1):
        '''
        Calculate the area or mass(if the area density is given) of a specific spherical polygon over a sphere with a radius of R. 
    
        Usage: 
        area = polygon.area()
        area = polygon.area(6378.137)

        Parameters:
        R -> [optional, float, default = 1] sphere radius
        rho -> [optional, float, default = 1] area density of the spherical polygon
        
        Outputs:
        area -> [float] Area of the spherical polygon. It is independent of how the vertices are arranged.
        ''' 
        return polygon_area(self.polygon)*R**2*rho

    def inertia(self, R = 1, rho = 1):
        '''
        Calculate the geometrical or physical(if the area density is given) moment of inertia tensor of a specific spherical polygon over a sphere with a radius of R.

        Usage:
        inertia = polygon.inertia()
        inertia = polygon.inertia(6378.137,81)

        Parameters:
        R -> [optional, float, default = 1] sphere radius
        rho -> [optional, float, default = 1] area density of the spherical polygon

        Outputs:
        inertia -> [float array with 6 elements] symmetrical inertia tensor with six independent components.
        The first three components are located diagonally, corresponding to M_{11}, M_{22}, and M_{33}; the last three components correspond to M_{12}, M_{13}, and M_{23}.
        '''
        return polygon_inertia(self.polygon)*R**4*rho 	

            
