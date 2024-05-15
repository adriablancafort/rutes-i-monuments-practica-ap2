import math
from segments import Point

def latlon_to_xy(point: Point) -> tuple[int,int]:
    # Coordinates of Barcelona
    lat_ref, lon_ref = 41.3851, 2.1734
    # Earth's radius in meters
    R = 6371000  
    # Convert degrees to radians
    lat = math.radians(point.lat)
    lon = math.radians(point.lon)
    lat_ref = math.radians(lat_ref)
    lon_ref = math.radians(lon_ref)
    
    # Average latitude calculation
    lat_avg = (point.lat + point.lat_ref) / 2
    
    # Calculate x and y
    x = (point.lon - lon_ref) * R * math.cos(lat_avg)
    y = (point.lat - lat_ref) * R
    
    return x, y

def xy_to_latlon(x, y) -> Point:
    # Coordinates of Barcelona
    lat_ref, lon_ref = 41.3851, 2.1734
    
    # Earth's radius in meters
    R = 6371000  
    # Convert reference lat and lon to radians
    lat_ref = math.radians(lat_ref)
    lon_ref = math.radians(lon_ref)
    
    # Average latitude used in the reverse calculation
    lat_avg = lat_ref + y / R
    
    # Calculate lat and lon from x and y
    lat = lat_ref + y / R
    lon = lon_ref + x / (R * math.cos(lat_avg))
    
    # Convert radians back to degrees
    lat = math.degrees(lat)
    lon = math.degrees(lon)
    
    return Point(lat,lon)



def centroid(coordinates: list[tuple[int,int]]) -> tuple[int,int]:
   
    sum_x: int = 0
    sum_y: int = 0    
    for x, y in coordinates:
        sum_x += x
        sum_y += y
    
    centroid_x = sum_x / len(coordinates)
    centroid_y = sum_y / len(coordinates)
    
    return (centroid_x, centroid_y)
