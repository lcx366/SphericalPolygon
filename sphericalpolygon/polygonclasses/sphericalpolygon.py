import numpy as np

from ..inside_polygon import inside_polygon
from ..excess_area import polygon_excess,polygon_area
from ..perimeter import polygon_perimeter
from ..centroid import polygon_centroid
from ..inertia import polygon_inertia

class Sphericalpolygon(object):
    '''
    class Sphericalpolygon

    - attributes:
        - vertices: vertices of a closed spherical polygon in form of [[lat_0,lon_0],...,[lat_n,lon_n]]
        - lats: latitudes of the spherical polygon in degrees
        - lons: longitudes of the spherical polygon in degrees
        - orientation: vertices arrangement; it can be counterclockwise or clockwise

    - methods:
        - contains_points: determine if a single point or multiple points are inside a spherical polygon.
        - area: calculate the area or mass of a spherical polygon.
        - perimeter: calculate the perimeter of a spherical polygon.
        - centroid: identify the location of the centroid of a spherical polygon.
        - inertia: compute the geometrial or physical moment of inertia tensor of a spherical polygon.
        
    '''

    def __init__(self, vertices: np.ndarray):
        """
        Initializes a SphericalPolygon instance.

        Inputs:
            vertices -> [array-like] Polygon vertices with shape (M, 2), where each row is [latitude, longitude] in degrees.
            The polygon does not need to be explicitly closed.
        """
        self.vertices = vertices
        self.lats = vertices[:, 0]
        self.lons = vertices[:, 1]

        # Automatic Orientation Detection
        excess = polygon_excess(self.vertices)

        if (0 < excess < 2 * np.pi) or (excess < -2 * np.pi):
            self.orientation = 'Counterclockwise'
        elif (-2 * np.pi < excess < 0) or (excess > 2 * np.pi):
            self.orientation = 'Clockwise'
        else:
            self.orientation = 'Undefined'

    def __repr__(self) -> str:
        """
        Provides an informative string representation of the SphericalPolygon object.

        This representation includes the polygon's orientation and whether it contains
        the North and South celestial poles.
        """
        # Define points for the North and South poles.
        pole_points = np.array([[90.0, 0.0], [-90.0, 0.0]])

        # Check for containment.
        inside_flags = self.contains_points(pole_points)

        return (
            f"<SphericalPolygon | ORIENTATION='{self.orientation}', "
            f"NorthPoleInside={inside_flags[0]}, "
            f"SouthPoleInside={inside_flags[1]}>"
        )

    def from_array(vertices):   
        '''
        Create an instance of class Sphericalpolygon from numpy array.
    
        Usage:
        polygon = Sphericalpolygon.from_array(vertices)

        Inputs:
        vertices -> [float 2d array] Vertices that make up the polygon in form of [[lat_0,lon_0],...,[lat_n,lon_n]] with unit of degrees. 
        If the first vertex is not equal to the last one, a point is automatically added to the end of the vertices sequence to form a closed polygon. 
        Vertices can be arranged either counterclockwise or clockwise.

        Outputs:
        polygon -> an instance of class Sphericalpolygon 

        Note: The spherical polygon has a latitude range of [-90°,90°] and a longitude range of [-180°,180°] or [0°,360°].
        '''
        closed_vertices = np.array(vertices)
        if (vertices[0] != vertices[-1]).any():
            # Close the polygon by appending the first vertex to the end.
            closed_vertices = np.vstack([vertices, vertices[0]])

        return Sphericalpolygon(closed_vertices)
    
    def from_file(filename,skiprows=0):
        '''
        Create an instance of class Sphericalpolygon from a file.
    
        Usage:
        polygon = Sphericalpolygon.from_file(filename,[skiprows])

        Inputs:
        filename -> [str] input file that lists vertices of a polygon in form of 

            # polygon info, such as name, and soure, etc.
            # comments
            #
            lat_0,lon_0
            ...
            lat_n,lon_n 

        with unit of degrees. If the first vertex is not equal to the last one, a point is automatically added to the end of the vertices sequence to form a closed polygon. 
        Vertices can be arranged either counterclockwise or clockwise.

        Parameters:
        skiprows -> [int, optional] skip the first `skiprows` lines, including comments; default: 0.

        Outputs:
        polygon -> an instance of class Sphericalpolygon 

        Note: The spherical polygon has a latitude range of [-90°,90°] and a longitude range of [-180°,180°] or [0°,360°].
        '''
        vertices = np.loadtxt(filename,skiprows=skiprows) 
        if (vertices[0] != vertices[-1]).all():
            vertices = np.append(vertices,[vertices[0]],axis=0) # create a closed spherical polygon

        return Sphericalpolygon(vertices)

    def contains_points(self,points):
        """
        Checks if one or more points are inside this spherical polygon.

        This method serves as a convenient wrapper around the core `inside_polygon`
        workhorse function, using the polygon's stored vertices and orientation.

        Inputs:
            points -> [np.ndarray] An array of points to check, with shape (N, 2). Each row is [latitude, longitude] in degrees.

        Returns:
            flags -> [np.ndarray] A boolean array of shape (N,), where `True` indicates the corresponding point is inside the polygon.

        Examples:
            >>> # Check one point
            >>> polygon.contains_points([[10, 20]])
            >>> # Check multiple points
            >>> test_points = [[10, 20], [50, 50]]
            >>> polygon.contains_points(test_points)
        """
        vertices = self.vertices
        orientation = self.orientation
        flags = inside_polygon(points,vertices,orientation)
        return flags

    def area(self, R = 1,rho = 1):
        '''
        Calculate the area or mass(if the area density is given) of a specific spherical polygon over a sphere with a radius of R. 
    
        Usage: 
        area = polygon.area()
        area = polygon.area(6378.137)
        mass = polygon.area(6378.137,81)

        Parameters:
        R -> [optional, float, default = 1] sphere radius
        rho -> [optional, float, default = 1] area density of the spherical polygon
        
        Outputs:
        area -> [float] Area of the spherical polygon. It is independent of how the vertices are arranged.
        ''' 
        return polygon_area(self.vertices)*R**2*rho

    def perimeter(self, R = 1):
        '''
        Calculate the perimeter of a spherical polygon over a sphere with a radius of R. 
    
        Usage: 
        peri = polygon.perimeter()
        peri = polygon.perimeter(6378.137)

        Parameters:
        R -> [optional, float, default = 1] sphere radius
        
        Outputs:
        perimeter -> [float] Perimeter of the spherical polygon. It is independent of how the vertices are arranged.
        ''' 
        return polygon_perimeter(self.vertices)*R   

    def compactness(self):
        '''
        Calculate the compactness(circularity) of a spherical polygon, which finds the deviation of a polygon from a spherical cap.
    
        Usage: 
        compactness = polygon.compactness()
        
        Outputs:
        compactness -> [float] a dimensional value. It takes a maximum value of 1 for a spherical cap.
        ''' 
        area = self.area()
        perimeter = self.perimeter()
        return area/perimeter**2*(4*np.pi - area)
        
    def centroid(self, R = 1):
        '''
        Identify the location of the centroid of a spherical polygon over a sphere with a radius of R. 
    
        Usage: 
        peri = polygon.centroid()
        peri = polygon.centroid(6378.137)

        Parameters:
        R -> [optional, float, default = 1] sphere radius
        
        Outputs:
        lat,lon,depth -> [float array with 3 elements] coordinate of the centroid. 
        Lat and lon are both in degrees; depth should be always positive, which implies the centroid is beneath the 'ground'.
        ''' 
        lat,lon,depth = polygon_centroid(self.vertices)
        return lat,lon,depth*R

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
        return polygon_inertia(self.vertices)*R**4*rho 	


            
