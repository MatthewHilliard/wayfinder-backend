from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from cities_light.models import City, Country

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def city_search(request):
    query = request.GET.get('q', '')  # Get the search query
    
    data = [] # Declare initial data list
    
    if not query:
        # Prepopulate with popular countries when the query is empty
        popular_countries = Country.objects.filter(name__in=[
            "United States", "Canada", "China", "United Kingdom", "Australia", "Germany"
        ])
        
        for country in popular_countries:
            data.append({
                "id": f"country-{country.id}",
                "type": "country",
                "name": country.name,
                "region": None,
                "country": country.name,
            })
        return JsonResponse(data, safe=False)
    
    # Match countries
    countries = Country.objects.filter(name__icontains=query)[:5]
    
    # Match cities with their associated regions and countries
    cities = City.objects.filter(name__icontains=query).select_related('region', 'country')[:10]
    
    # Combine Results
    for country in countries:
        data.append({
            "id": f"country-{country.id}",
            "type": "country",
            "name": country.name,
            "region": None,
            "country": country.name,
        })

    for city in cities:
        data.append({
            "id": f"city-{city.id}",
            "type": "city",
            "name": city.name,
            "region": city.region.name if city.region else None,
            "country": city.country.name if city.country else None,
        })

    return JsonResponse(data, safe=False)