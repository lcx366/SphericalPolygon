import numpy as np
from scipy.integrate import dblquad
from astropy.coordinates import cartesian_to_spherical
from astropy import units as u
from .excess_area import polygon_excess
from .functions import *

def polygon_centroid(vertices):
    '''
    Calculate the centroid of a spherical polygon over a unit sphere.

    Usage:
    inertia = polygon_centroid(vertices)

    Inputs:
    vertices -> [float 2d array] Vertices of the spherical polygon in form of [[lat_0,lon_0],..,[lat_n,lon_n]] with unit of degrees.
    Vertices can be arranged either counterclockwise or clockwise.

    Outputs:
    lat,lon,depth -> [float array with 3 elements] centroid location with lat and lon in degrees, and depth less than 1

    Note: The spherical polygon has a latitude range of [-90°,90°] and a longitude range of [-180°,180°] or [0°,360°].
    ''' 
    N = len(vertices)
    
    # Initialize the 3 components of the centroid coordinate
    sumx,sumy,sumz = np.zeros(3)

    for i in range(N - 1):
        p1 = np.radians(vertices[i])
        p2 = np.radians(vertices[i+1]) 
        
        pdlon = p2[1]-p1[1]
        if pdlon < -np.pi: p2[1] = p2[1] + 2*np.pi 
        if pdlon > np.pi: p2[1] = p2[1] - 2*np.pi 
 
        # If two adjacent vertices are close enough(coincident), do nothing. 
        if np.abs(pdlon)  < 1e-6: continue 
            
        c1,c2,c3= integrate_coeffs(p1,p2)    

        # Calculate the centroid coordinate
        sx = dblquad(fx, p1[1], p2[1], fs_low,fs_up)
        sy = dblquad(fy, p1[1], p2[1], fs_low,fs_up)
        sz = dblquad(fz, p1[1], p2[1], fs_low,fs_up)
        
        sumx += sx[0] 
        sumy += sy[0]
        sumz += sz[0] 
        
    excess = polygon_excess(vertices)    
  
    # For counterclockwise arrangement
    if excess > 0 and excess < 2*np.pi: 
        centroidx = sumx/excess 
        centroidy = sumy/excess 
        centroidz = sumz/excess 
        
    if excess >= 2*np.pi:  
        centroidx = -sumx/(4*np.pi - excess)
        centroidy = -sumy/(4*np.pi - excess)
        centroidz = -sumz/(4*np.pi - excess) 
    
    # For clockwise arrangement
    if excess < 0 and excess > -2*np.pi: 
        centroidx = sumx/excess 
        centroidy = sumy/excess 
        centroidz = sumz/excess 

    if excess <= -2*np.pi: 
        centroidx = sumx/(4*np.pi + excess)
        centroidy = sumy/(4*np.pi + excess)
        centroidz = sumz/(4*np.pi + excess)

    r,lat,lon = cartesian_to_spherical(centroidx,centroidy,centroidz) 
    depth = 1 - r
    lat,lon = lat.to(u.deg).value,lon.to(u.deg).value 
     
    return np.array([lat,lon,depth])