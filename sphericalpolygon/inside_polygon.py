import numpy as np
from scipy.spatial.transform import Rotation
from astropy.coordinates import spherical_to_cartesian,cartesian_to_spherical
from astropy import units as u

def inside_polygon(point,vertices,arrangement):
    '''
    Determine if a single point is inside a spherical polygon.

    Usage: 
    flag = inside_polygon(point,vertices)

    Inputs:
    point -> [float array with 2 elements] Point to be determined in form of [lat,lon] with unit of degrees.
    vertices -> [float 2d array] Vertices of a spherical polygon in form of [[lat_0,lon_0],..,[lat_n,lon_n]] with unit of degrees.
    arrangement -> [str] Arrangement of the vertices. Avaliable options are Counterclockwise and Clockwise.

    Outputs:
    flag -> [bool] If True, the point is inside the polygon, otherwise, it is outside.

    Note: The spherical polygon has a latitude range of [-90°,-90°] and a longitude range of [-180°,180°] or [0°,360°].
    '''
    N = len(vertices)
    lat0,lon0 = point[0],point[1]
    lats,lons = vertices[:,0],vertices[:,1]

    # Rotate the single point and polygon so that the North Pole axis passes through the single point.
    transform = Rotation.from_euler('zy', [-lon0,lat0 - 90], degrees=True)
    polygon_cartesian = spherical_to_cartesian(np.ones(N),lats*u.deg,lons*u.deg)
    polygon_cartesian_transformed = transform.apply(np.stack(polygon_cartesian).T)
    xs,ys,zs = [polygon_cartesian_transformed[:,i] for i in range(3)]
    polygon_spherical_transformed = cartesian_to_spherical(xs,ys,zs)

    lons_transformed = polygon_spherical_transformed[2].value # unit in rad
    
    sum_angle = 0
    flag = False

    for i in range(N-1):
        dlon = lons_transformed[i+1] - lons_transformed[i]
        if dlon > np.pi: dlon = -2*np.pi + dlon  
        if dlon < -np.pi: dlon = 2*np.pi + dlon
        sum_angle += dlon

    # The single point and the sides of the polygon form N spherical triangles.
    # If the single point is inside the counterclockwise polygon, the sum of the opposite angles should be 2π. 
    if arrangement == 'Counterclockwise':
        if np.abs(sum_angle - 2*np.pi) < 0.1: flag = True
    # If the single point is inside the clockwise polygon, the sum of the opposite angles should be -2π.     
    elif arrangement == 'Clockwise':   
        if np.abs(sum_angle + 2*np.pi) < 0.1: flag = True
    else:
    	raise Exception('Arrangement of the vertices can either be Counterclockwise or Clockwise.')
    return flag