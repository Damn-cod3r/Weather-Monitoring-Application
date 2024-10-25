from background_task import background
from .utils import fetch_weather_data, aggregate_daily_weather


@background(schedule=300)  # Schedule every 300 seconds or 5 minutes
def update_weather_data():
    fetch_success = fetch_weather_data()
    if fetch_success:
        aggregate_daily_weather()  # Aggregate after fetching