import requests


def get_location_api(location):
    url = "https://db.ou.org/location" + f"?city={location}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP error responses
        data = response.json() 
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        timezone = data.get('timezone')
        return latitude, longitude, timezone
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None, None, None