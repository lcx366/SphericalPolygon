# Welcome to the SphericalPolygon package

The SphericalPolygon package is an archive of scientific routines for handling spherical polygons. Currently, operations on spherical polygons include calculating area or mass(if the area density is given), geometrical or physical moment of inertia tensor, and determining whether one or more points are inside the spherical polygon.

## How to Install

SphericalPolygon can be installed with `pip install sphericalpolygon`.

## How to use

### Create a spherical polygon

Spherical polygons can be created based on a self-defined 2d array in form of `[[lat_0,lon_0],..,[lat_n,lon_n]]` with unit of degrees or a boundary file, such as [Plate boundaries for NNR-MORVEL56 model](http://geoscience.wisc.edu/~chuck/MORVEL/PltBoundaries.html). The spherical polygon has a latitude range of [-90,90] and a longitude range of [-180,180] or [0,360].


```python
import numpy as np
from sphericalpolygon import create_polygon

boundary = np.loadtxt('NnrMRVL_PltBndsLatLon/an',skiprows=1) # boundary for Antarctica Plate
polygon = create_polygon(boundary)

print(polygon.arrangement)
```

    Counterclockwise


The results show that vertices of the spherical polygon are connected counterclockwise. For more details on attributes and methods of the polygon object, please refer to  `polygon?`.

### Calculate the area

Calculate the area of the spherical polygon over a unit sphere.


```python
print(polygon.area())
```

    1.4326235943514618


Calculate the area of the spherical polygon over a sphere with a radius of 6378.137km.


```python
print(polygon.area(6378.137), ' km2')
```

    58280032.6500551  km2


### Calculate the moment of inertia tensor

Calculate the geometrical moment of inertia tensor of the spherical polygon over a unit sphere. The tensor is symmetrical and has six independent components. The first three components are located diagonally, corresponding to $M_{11}$, $M_{22}$, and $M_{33}$; the last three components correspond to $M_{12}$, $M_{13}$, and $M_{23}$.


```python
print(polygon.inertia())
```

    [ 1.32669154  1.17471081  0.36384484 -0.05095381  0.05246122  0.08126929]


Calculate the moment of inertia tensor of the spherical polygon with an area density of 81Gt/km2 over a sphere with a radius of 6378.137km. 


```python
print(polygon.inertia(6378.127,81)/1e12, ' Gt·Gm2')
```

    [177839.25501653 157466.66651681  48772.37278617  -6830.21381414
       7032.2786668   10893.9188177 ]  Gt·Gm2


### Points are inside the polygon？

 Determine if a single point or multiple points are inside the given spherical polygon.

#### single point


```python
print(polygon.contains_points([75,152]))
```

    False


#### multiple points


```python
print(polygon.contains_points([[-85,130],[35,70]]))
```

    [True, False]


## Reference

[1] 李春晓.MORVEL 构造板块的转动惯量张量(英文)[J].天文研究与技术,2016,13(01):58-69.
