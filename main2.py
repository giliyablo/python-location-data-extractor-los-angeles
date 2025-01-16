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
    "Eaton Aerospace",
    "Eaton Canyon Nature Center",
    "Eaton",
    "Eat'n Park Restaurant",
    "Eaton Canyon",
    "Eaton Designs",
    "Easton-Rancho Park Archery Range",
    "Parking place for Eaton Canyon Falls",
    "Griffith Observatory",
    "Hurst Ranch Historical Center",
    "Stonehurst",
    "Whitehurst",
    "Ovation Hollywood",
    "Avila Adobe",
    "The Hoxton",
    "STILE Downtown Los Angeles by Kasa",
    "TCL Chinese Theatre",
    "Hilton Garden Inn Los Angeles/Hollywood",
    "Hollywood Sign",
    "Campo De Cahuenga",
    "Dolby Theatre",
    "Hertz Car Rental - Los Angeles - N Lacienega Boulevard",
    "Dr. Ronald Hurst",
    "HillHurst Tax Group",
    "Ronald Hurst",
    "North East Mall",
    "Taqueria Los Angeles",
    "Thai on Hillhurst",
    "Stonehurst Recreation Center",
    "Hirsch Pipe & Supply",
    "Palisades Park",
    "Temescal Canyon Park",
    "The Point at the Bluffs",
    "Pacific Palisades Beach",
    "SRF Lake Shrine (Reservation required)",
    "Spruzzo Restaurant & Bar",
    "Pacific Palisades",
    "Eagle Rock Trail Head",
    "The Cafe",
    "Will Rogers State Beach",
    "Juicy Ladies",
    "Golden Bull Restaurant",
    "Fiesta Feast",
    "Rocco's Cucina",
    "Palisades Park",
    "Annenberg Community Beach House",
    "Back on the Beach Cafe",
    "Huntington Palisades",
    "Santa Monica Pier",
    "Giorgio Baldi",
    "Venice Canal Historic District",
    "Eames Foundation",
    "Rustic Canyon",
    "MUSE Santa Monica",
    "Original Muscle Beach Santa Monica",
    "Santa Monica Pier Arch",
    "Santa Ynez Canyon Trailhead - Topanga State Park",
    "Venice Boardwalk",
    "Tongva Park",
    "ֳ‰lephante",
    "Caffֳ© Delfini",
    "Ye Olde King's Head",
    "Pacific Wheel",
    "Massilia",
    "Farmshop",
    "Maria Sol",
    "Las Tunas Beach",
    "Huckleberry Bakery & Cafe",
    "Franklin D. Murphy Sculpture Garden",
    "The Cheesecake Factory",
    "North Italia",
    "Domino's Pizza",
    "Santa Monica Beach",
    "West Coaster",
    "UOVO | Santa Monica",
    "Douglas Park",
    "Santa Monica Pier Carousel",
    "Universal Studios Hollywood",
    "Blue Plate Taco",
    "Hillstone",
    "Palisades Village",
    "Forma Restaurant & Cheese Bar Santa Monica",
    "The Courtyard Kitchen",
    "The Palisades Villa",
    "R+D Kitchen",
    "The Palisades",
    "Santa Monica Ghosts",
    "Old Santa Monica Forestry Station",
    "Rock N Pies",
    "A Votre Santé"
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
