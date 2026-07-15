import httpx


GEOCODING_URL = (
    "https://geocoding-api.open-meteo.com/v1/search"
)

WEATHER_URL = (
    "https://api.open-meteo.com/v1/forecast"
)


LOCATION_ALIASES = {
    "bangalore": "Bengaluru",
    "bangalore city": "Bengaluru",
    "bombay": "Mumbai",
    "madras": "Chennai",
    "calcutta": "Kolkata",
}


WEATHER_CODES = {
    0: "Clear sky ☀️",
    1: "Mainly clear 🌤️",
    2: "Partly cloudy ⛅",
    3: "Overcast ☁️",
    45: "Foggy 🌫️",
    48: "Foggy 🌫️",
    51: "Light drizzle 🌦️",
    53: "Drizzle 🌦️",
    55: "Heavy drizzle 🌧️",
    61: "Light rain 🌦️",
    63: "Rain 🌧️",
    65: "Heavy rain 🌧️",
    71: "Light snow 🌨️",
    73: "Snow 🌨️",
    75: "Heavy snow ❄️",
    80: "Rain showers 🌦️",
    81: "Rain showers 🌧️",
    82: "Heavy rain showers 🌧️",
    95: "Thunderstorm ⛈️",
    96: "Thunderstorm with hail ⛈️",
    99: "Heavy thunderstorm with hail ⛈️",
}


def normalize_location(location: str):
    cleaned_location = location.strip()

    normalized_key = cleaned_location.lower()

    return LOCATION_ALIASES.get(
        normalized_key,
        cleaned_location,
    )


async def get_location(location: str):
    search_location = normalize_location(location)

    print(
        f"Weather location search: "
        f"{location} -> {search_location}"
    )

    params = {
        "name": search_location,
        "count": 20,
        "language": "en",
        "format": "json",
    }

    try:
        async with httpx.AsyncClient(
            timeout=10.0
        ) as client:
            response = await client.get(
                GEOCODING_URL,
                params=params,
            )

            response.raise_for_status()

            data = response.json()

    except Exception as error:
        print(
            f"Geocoding request failed: {error}"
        )

        return None

    results = data.get("results", [])

    if not results:
        print(
            f"No location found for: "
            f"{search_location}"
        )

        return None

    print("Geocoding results:")

    for result in results:
        print(
            result.get("name"),
            result.get("admin1"),
            result.get("country"),
            result.get("country_code"),
        )

    indian_locations = [
        result
        for result in results
        if result.get("country_code") == "IN"
    ]

    if indian_locations:
        selected_location = indian_locations[0]

        print(
            "Selected Indian location:",
            selected_location.get("name"),
            selected_location.get("admin1"),
            selected_location.get("country"),
        )

        return selected_location

    selected_location = results[0]

    print(
        "Selected location:",
        selected_location.get("name"),
        selected_location.get("admin1"),
        selected_location.get("country"),
    )

    return selected_location


async def get_weather(location: str):
    location_data = await get_location(location)

    if not location_data:
        return None

    latitude = location_data.get("latitude")

    longitude = location_data.get("longitude")

    city = location_data.get(
        "name",
        location,
    )

    country = location_data.get(
        "country",
        "",
    )

    admin1 = location_data.get(
        "admin1",
        "",
    )

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "apparent_temperature,"
            "relative_humidity_2m,"
            "precipitation,"
            "weather_code,"
            "wind_speed_10m"
        ),
        "timezone": "auto",
    }

    try:
        async with httpx.AsyncClient(
            timeout=10.0
        ) as client:
            response = await client.get(
                WEATHER_URL,
                params=params,
            )

            response.raise_for_status()

            data = response.json()

    except Exception as error:
        print(
            f"Weather request failed: {error}"
        )

        return None

    current = data.get("current", {})

    temperature = current.get(
        "temperature_2m"
    )

    feels_like = current.get(
        "apparent_temperature"
    )

    humidity = current.get(
        "relative_humidity_2m"
    )

    precipitation = current.get(
        "precipitation"
    )

    wind_speed = current.get(
        "wind_speed_10m"
    )

    weather_code = current.get(
        "weather_code"
    )

    condition = WEATHER_CODES.get(
        weather_code,
        "Unknown weather",
    )

    location_name = city

    if admin1:
        location_name += f", {admin1}"

    if country:
        location_name += f", {country}"

    weather_message = (
        f"🌤️ Weather in {location_name}\n\n"
        f"🌡️ Temperature: {temperature}°C\n"
        f"🤗 Feels like: {feels_like}°C\n"
        f"💧 Humidity: {humidity}%\n"
        f"🌧️ Precipitation: {precipitation} mm\n"
        f"💨 Wind speed: {wind_speed} km/h\n"
        f"☁️ Condition: {condition}"
    )

    return weather_message