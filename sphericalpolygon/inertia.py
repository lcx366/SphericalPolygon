import numpy as np
from scipy.integrate import dblquad
from .excess_area import polygon_excess
from .functions import *

def polygon_inertia(vertices):
    '''
    Calculate the geometrical inertia tensor of a spherical polygon over a unit sphere.

    Usage:
    inertia = polygon_inertia(vertices)

    Inputs:
    vertices -> [float 2d array] Vertices of the spherical polygon in form of [[lat_0,lon_0],..,[lat_n,lon_n]] with unit of degrees.
    Vertices can be arranged either counterclockwise or clockwise.

    Outputs:
    inertia -> [float array with 6 elements] geometrical inertia tensor; it is symmetrical and has six independent components.

    Note: The spherical polygon has a latitude range of [-90°,90°] and a longitude range of [-180°,180°] or [0°,360°].
    ''' 
    N = len(vertices)
    
    # Initialize the 6 components of the geometrical inertia tensor
    sum11,sum22,sum33,sum12,sum13,sum23 = np.zeros(6)

    for i in range(N - 1):
        p1 = np.radians(vertices[i])
        p2 = np.radians(vertices[i+1]) 
        
        pdlon = p2[1]-p1[1]
        if pdlon < -np.pi: p2[1] = p2[1] + 2*np.pi 
        if pdlon > np.pi: p2[1] = p2[1] - 2*np.pi 
 
        # If two adjacent vertices are close enough(coincident), do nothing. 
        if np.abs(pdlon)  < 1e-6: continue 
            
        c1,c2,c3= integrate_coeffs(p1,p2)    

        # Calculate the geometrical inertia tensor 
        s11 = dblquad(f11, p1[1], p2[1], fs_low,fs_up)
        s22 = dblquad(f22, p1[1], p2[1], fs_low,fs_up)
        s33 = dblquad(f33, p1[1], p2[1], fs_low,fs_up)
        s12 = dblquad(f12, p1[1], p2[1], fs_low,fs_up)
        s13 = dblquad(f13, p1[1], p2[1], fs_low,fs_up)
        s23 = dblquad(f23, p1[1], p2[1], fs_low,fs_up)
        
        sum11 += s11[0] 
        sum22 += s22[0]
        sum33 += s33[0] 
        sum12 += s12[0] 
        sum13 += s13[0] 
        sum23 += s23[0] 
        
    excess = polygon_excess(vertices)    
  
    # For counterclockwise arrangement
    if excess > 0 and excess < 2*np.pi: 
        inertia11 = excess - sum11 
        inertia22 = excess - sum22 
        inertia33 = excess - sum33 
        
        inertia12 = -sum12 
        inertia13 = -sum13 
        inertia23 = -sum23 
        
    if excess >= 2*np.pi:  
        inertia11 = 8/3*np.pi - (excess - sum11)
        inertia22 = 8/3*np.pi - (excess - sum22)
        inertia33 = 8/3*np.pi - (excess - sum33) 
    
        inertia12 = sum12 
        inertia13 = sum13 
        inertia23 = sum23 
    
    # For clockwise arrangement
    if excess < 0 and excess > -2*np.pi: 
        inertia11 = -excess + sum11
        inertia22 = -excess + sum22
        inertia33 = -excess + sum33 
        
        inertia12 = sum12 
        inertia13 = sum13 
        inertia23 = sum23 
        
    if excess <= -2*np.pi: 
        inertia11 = 8/3*np.pi - (-excess + sum11)
        inertia22 = 8/3*np.pi - (-excess + sum22)
        inertia33 = 8/3*np.pi - (-excess + sum33)
        
        inertia12 = -sum12 
        inertia13 = -sum13 
        inertia23 = -sum23 
    
    return np.array([inertia11,inertia22,inertia33,inertia12,inertia13,inertia23])