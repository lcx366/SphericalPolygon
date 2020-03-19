import numpy as np
from .functions import hav

def polygon_excess(vertices):
    '''
    Calculate the signed area of a spherical polygon over a unit sphere. 
    
    Usage: 
    signed_area = polygon_excess(vertices)

    Inputs:
    vertices -> [float 2d array] Vertices of the spherical polygon in form of [[lat_0,lon_0],..,[lat_n,lon_n]] with unit of degrees.
    Vertices can be arranged either counterclockwise or clockwise.
    
    Outputs:
    signed_area -> [float] The signed area of a spherical polygon in steradians.
    For the case where the South Pole is outside the polygon, if the arrangement of the vertices is counterclockwise, the signed area should be positive, otherwise, it should be negative. 
    For the case where the South Pole is inside the polygon, if the arrangement of the vertices is counterclockwise, the signed area should be negative, otherwise, it should be positive.
    
    Note: The spherical polygon has a latitude range of [-90°,90°] and a longitude range of [-180°,180°] or [0°,360°].
    ''' 
    N = len(vertices)

    sum_excess = 0
    
    for i in range(N-1):
        p1,p2 = np.radians(vertices[i]),np.radians(vertices[i+1]) 
        pdlat,pdlon = p2[0] - p1[0], p2[1] - p1[1] 
        dlon = np.abs(pdlon) 
        
        # If two adjacent vertices are close enough(coincident), do nothing. 
        if dlon < 1e-6: continue 

        # Calculate the area of a spherical triangle consisting of sides and north poles  
        if dlon > np.pi: dlon = 2*np.pi - dlon 
        if pdlon < -np.pi: p2[1] = p2[1] + 2*np.pi 
        if pdlon > np.pi: p2[1] = p2[1] - 2*np.pi 
        
        havb = hav(pdlat) + np.cos(p1[0])*np.cos(p2[0])*hav(dlon) 
        b = 2*np.arcsin(np.sqrt(havb)) 
        a,c = np.pi/2 - p1[0], np.pi/2 - p2[0] 
        s = 0.5*(a + b + c) 
        t = np.tan(s/2)*np.tan((s - a)/2)*np.tan((s - b)/2)*np.tan((s - c)/2) 
        excess = 4*np.arctan(np.sqrt(np.abs(t)))
        if p2[1] - p1[1] < 0: excess = -excess 
    
        sum_excess += excess 

    return sum_excess

def polygon_area(vertices):
    '''
    Calculate the area of a spherical polygon over a unit sphere.
    
    Usage: 
    area = polygon_area(vertices)

    Inputs:
    vertices -> [float 2d array] Vertices of a spherical polygon in format of [[lat_0,lon_0],..,[lat_n,lon_n]] with unit of degrees.
    Vertices can be arranged either counterclockwise or clockwise.
    
    Outputs:
    area -> [float] Area of the spherical polygon in steradians. It is independent of how the vertices are arranged.

    Note: The spherical polygon has a latitude range of [-90,90] and a longitude range of [-180,180] or [0,360].
    ''' 
    excess = polygon_excess(vertices)
    area = np.abs(excess)
    
    if area > 2*np.pi: area = 4*np.pi - area

    return area