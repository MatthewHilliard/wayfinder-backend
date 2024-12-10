"""
Author: Matthew Hilliard
Email: mch2003@bu.edu
Description: This module provides helper functions, currently just `find_nearest_city`, which attempts to locate 
the nearest city to a given latitude and longitude by incrementally expanding the search range.
"""

from cities_light.models import City

def find_nearest_city(latitude, longitude, max_attempts=5, increment=0.5):
    """
    Attempt to find the nearest city by incrementally expanding the search range.

    Parameters:
        latitude (float): The latitude to search from.
        longitude (float): The longitude to search from.
        max_attempts (int): The maximum number of incremental search attempts.
        increment (float): The amount to expand the search range on each attempt.

    Returns:
        City or None: The nearest city found within the search range, or None if no city is found.
    """
    for attempt in range(max_attempts):
        range_increment = increment * (attempt + 1)
        city = City.objects.filter(
            latitude__range=(latitude - range_increment, latitude + range_increment),
            longitude__range=(longitude - range_increment, longitude + range_increment)
        ).first()
        if city:
            return city
    return None