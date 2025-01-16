import requests
import os

# API key from the environment variable
API_KEY = os.getenv("GOOGLE_API_KEY")

# Function to fetch places using Text Search with pagination
def fetch_places(query, page_token=""):
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={API_KEY}"
    if page_token:
        url += f"&pagetoken={page_token}"
    response = requests.get(url).json()
    return response

# Function to fetch place details (opening hours, popular times)
def get_place_details(place_id):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={API_KEY}"
    response = requests.get(url).json()
    return response["result"]

# Function to process a single area (neighborhood or zip code)
def process_area(area_name):
    csv_data = []
    csv_data.append([
        "Name",
        "Address",
        "Latitude",
        "Longitude",
        "Opening Hours",
        "Popular Times",
        "Secondary Opening Hours",
        "Open Now",
        "Current Opening Hours",
    ])

    next_page_token = ""
    while True:
        query = f"places in {area_name}, Los Angeles"
        data = fetch_places(query, next_page_token)

        for place in data["results"]:
            try:
                details = get_place_details(place["place_id"])

                # Fetch popular times
                popular_times_data = "N/A"
                try:
                    popular_times_data = populartimes.full_week(place["place_id"])
                    print("🚀", popular_times_data)
                except Exception as e:
                    print(f"Error fetching popular times for {place['name']}:", e)

                # Extract opening hours
                opening_hours = "N/A"
                if details.get("opening_hours") and details["opening_hours"].get("weekday_text"):
                    opening_hours = "; ".join(details["opening_hours"]["weekday_text"])

                # Extract secondary opening hours if available
                secondary_opening_hours = "N/A"
                if (
                    details.get("opening_hours")
                    and details["opening_hours"].get("periods")
                    and len(details["opening_hours"]["periods"]) > 1
                ):
                    secondary_opening_hours = (
                        f"{details['opening_hours']['periods'][1]['open']['day']} {details['opening_hours']['periods'][1]['open']['time']} - {details['opening_hours']['periods'][1]['close']['time']}"
                    )

                # Check if place is open now
                open_now = "N/A"
                if details.get("opening_hours"):
                    open_now = "Yes" if details["opening_hours"]["open_now"] else "No"

                # Extract current opening hours
                current_opening_hours = "N/A"
                now = datetime.datetime.now()
                day_of_week = now.weekday()  # 0 (Sunday) to 6 (Saturday)
                if (
                    details.get("opening_hours")
                    and details["opening_hours"].get("periods")
                ):
                    for period in details["opening_hours"]["periods"]:
                        if period["open"]["day"] == day_of_week:
                            current_opening_hours = (
                                f"{period['open']['time']} - {period['close']['time']}"
                            )
                            break

            except Exception as e:
                print(f"Error fetching details for {place['name']}:", e)

            finally:
                csv_data.append([
                    place["name"],
                    place["formatted_address"],
                    place["geometry"]["location"]["lat"],
                    place["geometry"]["location"]["lng"],
                    opening_hours,
                    popular_times_data,
                    secondary_opening_hours,
                    open_now,
                    current_opening_hours,
                ])

            # Add a delay to avoid hitting rate limits
            time.sleep(2)

        next_page_token = data.get("next_page_token")
        if not next_page_token:
            break

        # Add a delay to avoid hitting rate limits
        time.sleep(2)

    # Write data to CSV file
    csv_content = "\n".join([",".join(row) for row in csv_data])
    with open(f"{area_name}_places.csv", "w", encoding="utf-8") as f:
        f.write(csv_content)

    print(f"CSV file created for {area_name}!")

# Function to save places data to CSV files
def save_places_to_csv():
    areas = ["Eaton", "Hurst", "Palisades"]  # Add more areas as needed

    for area in areas:
        process_area(area)

# Call the function to save places data to CSV files
save_places_to_csv()
