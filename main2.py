
# prompt: great. now with the current code, use the package ' populartimes' to get the popular times as well.

import googlemaps
import populartimes

# Replace 'YOUR_API_KEY' with your actual Google Maps API key
API_KEY = 'AIzaSyAds_b06QIxqMmv36dyN6gpXuZ-SYj5BGM'
gmaps = googlemaps.Client(key='AIzaSyAds_b06QIxqMmv36dyN6gpXuZ-SYj5BGM')

def get_place_details(place_name, location):
    """
    Get details of a place including opening hours and popular times.
    :param place_name: The name of the place to search for.
    :param location: Location bias (latitude, longitude).
    :return: Place details dictionary.
    """
    # Perform a place search
    search_results = gmaps.places(query=place_name, location=location)
    
    if 'results' in search_results and search_results['results']:
        place_id = search_results['results'][0]['place_id']  # Get the place ID
        # Fetch place details
        place_details = gmaps.place(place_id=place_id)
        
        # Get popular times using the populartimes library
        try:
          popular_times = populartimes.get_id(API_KEY, place_id)
          if popular_times:
            place_details['result']['populartimes'] = popular_times['populartimes']
        except Exception as e:
          print(f"Error getting popular times: {e}")
          
        return place_details.get('result', {})
    else:
        return None

# Example usage
place_name = "Hollywood Walk of Fame"
location = (34.101, -118.341)  # Coordinates for Los Angeles, CA
details = get_place_details(place_name, location)

if details:
    print("Name:", details.get('name'))
    print("Address:", details.get('formatted_address'))
    print("Opening Hours:", details.get('opening_hours', {}).get('weekday_text', 'Not available'))
    print("Popular Times:", details.get('populartimes', 'Not available'))
else:
    print("Place not found.")
