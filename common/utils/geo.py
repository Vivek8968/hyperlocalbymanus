import math
from typing import Optional, List, Tuple
from geopy.distance import geodesic

class GeoService:
    """
    Service for geolocation operations
    """
    @staticmethod
    async def calculate_distance(
        lat1: float, 
        lon1: float, 
        lat2: float, 
        lon2: float
    ) -> float:
        """
        Calculate distance between two points in kilometers
        """
        point1 = (lat1, lon1)
        point2 = (lat2, lon2)
        
        # Calculate distance using geodesic
        distance = geodesic(point1, point2).kilometers
        return distance
    
    @staticmethod
    async def sort_by_distance(
        reference_lat: float,
        reference_lon: float,
        locations: List[dict]
    ) -> List[dict]:
        """
        Sort locations by distance from reference point
        
        Each location dict must have 'latitude' and 'longitude' keys
        Returns locations with added 'distance' key
        """
        for location in locations:
            distance = await GeoService.calculate_distance(
                reference_lat,
                reference_lon,
                location['latitude'],
                location['longitude']
            )
            location['distance'] = round(distance, 2)
        
        # Sort by distance
        sorted_locations = sorted(locations, key=lambda x: x['distance'])
        return sorted_locations
    
    @staticmethod
    async def filter_by_radius(
        reference_lat: float,
        reference_lon: float,
        locations: List[dict],
        radius_km: float
    ) -> List[dict]:
        """
        Filter locations within specified radius in kilometers
        
        Each location dict must have 'latitude' and 'longitude' keys
        Returns filtered locations with added 'distance' key
        """
        result = []
        for location in locations:
            distance = await GeoService.calculate_distance(
                reference_lat,
                reference_lon,
                location['latitude'],
                location['longitude']
            )
            
            if distance <= radius_km:
                location['distance'] = round(distance, 2)
                result.append(location)
        
        # Sort by distance
        sorted_result = sorted(result, key=lambda x: x['distance'])
        return sorted_result
