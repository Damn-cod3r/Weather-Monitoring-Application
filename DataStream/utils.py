# weather/utils.py
import requests
from django.conf import settings
from django.utils import timezone  # Import timezone utilities
from .models import WeatherData, DailyWeatherSummary
from datetime import datetime, timezone as dt_timezone  # Use dt_timezone to avoid conflicts
from django.db.models import Avg, Max, Min, Count
from datetime import timedelta

def fetch_weather_data(city='London'):
    api_key = settings.OPENWEATHER_API_KEY
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Extract relevant fields
        weather_main = data['weather'][0]['main']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        dt = datetime.utcfromtimestamp(data['dt'])  # Convert UNIX timestamp

        # Convert to timezone-aware datetime
        dt_aware = timezone.make_aware(dt, dt_timezone.utc)  # Use datetime.timezone.utc

        # Save to the database
        WeatherData.objects.create(main=weather_main, temp=temp, feels_like=feels_like, dt=dt_aware)
        return True  # Indicate successful save

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return False  # Indicate failure


def aggregate_daily_weather():
    today = timezone.now().date()  # Get today's date
    # Get all weather data for today
    today_weather_data = WeatherData.objects.filter(dt__date=today)

    if not today_weather_data.exists():
        print("No weather data available for today.")
        return

    # Calculate aggregates
    avg_temp = today_weather_data.aggregate(Avg('temp'))['temp__avg']
    max_temp = today_weather_data.aggregate(Max('temp'))['temp__max']
    min_temp = today_weather_data.aggregate(Min('temp'))['temp__min']
    
    # Determine dominant condition
    dominant_condition = today_weather_data.values('main').annotate(count=Count('main')).order_by('-count').first()

    # Create or update DailyWeatherSummary
    DailyWeatherSummary.objects.update_or_create(
        date=today,
        defaults={
            'avg_temp': avg_temp,
            'max_temp': max_temp,
            'min_temp': min_temp,
            'dominant_condition': dominant_condition['main'] if dominant_condition else 'N/A',
        }
    )

    print("Daily weather summary updated.")