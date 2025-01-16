import googlemaps
import populartimes
import csv

# Replace 'YOUR_API_KEY' with your actual Google Maps API key
API_KEY = 'AIzaSyAds_b06QIxqMmv36dyN6gpXuZ-SYj5BGM'
gmaps = googlemaps.Client(key=API_KEY)

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

# List of places in Los Angeles
places = [
    "Hollywood Walk of Fame",
    "Universal Studios Hollywood",
    "The Getty Museum",
    "Santa Monica Pier",
    "Venice Beach",
    "Griffith Observatory",
    "The Broad Museum",
    "Walt Disney Concert Hall",
    "LACMA (Los Angeles County Museum of Art)",
    "The Natural History Museum",
    "Dodger Stadium",
    "Runyon Canyon Park",
    "Hollywood Bowl",
    "TCL Chinese Theatre",
    "La Brea Tar Pits",
    "Grand Central Market",
    "Olvera Street",
    "California Science Center",
    "Exposition Park Rose Garden",
    "The Grove",
    "The Original Farmers Market",
    "Beverly Hills Rodeo Drive",
    "Hollywood Forever Cemetery",
    "Griffith Park",
    "Los Angeles Zoo",
    "Santa Monica State Beach",
    "Venice Canals",
    "Abbot Kinney Boulevard",
    "Manhattan Beach",
    "Hermosa Beach",
    "Redondo Beach Pier",
    "The Getty Villa",
    "Hammer Museum",
    "Museum of Contemporary Art (MOCA)",
    "Norton Simon Museum",
    "Huntington Library, Art Museum, and Botanical Gardens",
    "Descanso Gardens",
    "Hollywood Sign",
    "Santa Monica Mountains National Recreation Area",
    "Malibu Pier",
    "Zuma Beach",
    "El Matador State Beach"
]

# Open the CSV file for writing
with open('places.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Name', 'Address', 'Opening Hours', 'Popular Times']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Loop through each place and get its details
    for place in places:
        print(f"Getting details for {place}")
        details = get_place_details(place, (34.101, -118.341))  # Use the coordinates of Los Angeles

        if details:
            # Extract the required information
            name = details.get('name')
            address = details.get('formatted_address')
            opening_hours = details.get('opening_hours', {}).get('weekday_text', 'Not available')
            popular_times = details.get('populartimes', 'Not available')

            # Write the data to the CSV file
            writer.writerow({
                'Name': name,
                'Address': address,
                'Opening Hours': opening_hours,
                'Popular Times': popular_times
            })
            print("Data written to CSV.\n")
        else:
            print("Place not found.\n")
            