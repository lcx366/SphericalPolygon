import numpy as np

# Half-versed-sine
def hav(x): 
    return (1 - np.cos(x))/2   

# Integeral lowerlimit as a function of longitude.
def fs_low(lon): 
    return -np.arctan((c1*np.cos(lon)+c2*np.sin(lon))/c3)

# Integeral upperlimit as a function of longitude.
def fs_up(lon): 
    return np.pi/2

# Coefficients for determining the lowerlimit in inner integral. 
def integrate_coeffs(p1,p2): 
    global c1,c2,c3
    # p1:[lat_j,lon_j], p2:[lat_{j+1},lon_{j+1}]
    c1 = np.cos(p1[0])*np.sin(p1[1])*np.sin(p2[0])-np.cos(p2[0])*np.sin(p2[1])*np.sin(p1[0]) 
    c2 = np.cos(p2[0])*np.cos(p2[1])*np.sin(p1[0])-np.cos(p1[0])*np.cos(p1[1])*np.sin(p2[0]) 
    c3 = np.cos(p1[0])*np.cos(p2[0])*np.sin(p2[1]-p1[1]) 
    return c1,c2,c3

# Integrands corresponding to six components of the geometrical inertia tensor.
def f11(lat,lon): 
    return np.cos(lat)**3*np.cos(lon)**2

def f22(lat,lon): 
    return np.cos(lat)**3*np.sin(lon)**2

def f33(lat,lon): 
    return np.sin(lat)**2*np.cos(lat)

def f12(lat,lon): 
    return np.cos(lat)**3*np.cos(lon)*np.sin(lon)

def f13(lat,lon): 
    return np.cos(lat)**2*np.sin(lat)*np.cos(lon)

def f23(lat,lon): 
    return np.cos(lat)**2*np.sin(lat)*np.sin(lon)

def fx(lat,lon):
    return np.cos(lat)**2*np.cos(lon)  

def fy(lat,lon):
    return np.cos(lat)**2*np.sin(lon)         

def fz(lat,lon):
    return np.sin(2*lat)/2                        