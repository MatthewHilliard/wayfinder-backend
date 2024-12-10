"""
Author: Matthew Hilliard
Email: mch2003@bu.edu
Description: This module provides an API view for searching cities and countries. 
The `city_search` function retrieves matching countries and cities based on a search 
query and returns their details, including city name, region, and country, in a structured JSON response.
"""

from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from cities_light.models import Country, City
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny]) 
def city_search(request):
    """
    Search for cities and countries based on the provided query.
    """
    query = request.GET.get('q', '')  # Get the search query
    
    data = [] # Declare initial data list
    
    # Match countries
    countries = Country.objects.filter(name__icontains=query)[:5]
    
    # Match cities with their associated regions and countries
    cities = City.objects.filter(name__icontains=query).select_related('region', 'country')[:10]
    
    # Combine Results
    for country in countries:
        data.append({
            "city_id": country.id,
            "type": "country",
            "name": None,
            "region": None,
            "country": country.name,
        })

    for city in cities:
        data.append({
            "city_id": city.id,
            "type": "city",
            "name": city.name or None,
            "region": city.region.name if city.region else None,
            "country": city.country.name if city.country else None,
        })

    return JsonResponse({'data': data}, safe=False)
