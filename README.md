
---

# Real-Time Data Processing System for Weather Monitoring 📊🌦️

This project demonstrates how to build a Django-based weather monitoring application with **real-time data processing** and **aggregate calculations** for daily weather summaries. The application fetches data from the OpenWeatherMap API, stores it in a database, computes daily summaries, and visualizes trends.

---

### Table of Contents

1. **Project Setup**
2. **Fetching Data from OpenWeatherMap API**
3. **Storing Weather Data**
4. **Scheduling Data Fetching with Background Tasks**
5. **Admin Setup**
6. **Troubleshooting Common Issues**

---

### 1. Project Setup

**Create a Django project and app:**

```bash
django-admin startproject SkySense
cd SkySense
python manage.py startapp DataStream
```

**Install Required Packages:**

```bash
pip install django requests django-background-tasks
```

**Configure Settings:**

In `SkySense/settings.py`, add `DataStream` and `background_task` to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'DataStream',
    'background_task',
]
```

**Set Up Database & Timezone Settings:**

Configure time zone settings to handle timestamps properly.

```python
# settings.py
TIME_ZONE = 'UTC'
USE_TZ = True
```

Apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 2. Fetching Data from OpenWeatherMap API

**Get an API Key**: Sign up on OpenWeatherMap and get your API key.

Store the key in `settings.py`:

```python
# settings.py
OPENWEATHER_API_KEY = 'your_api_key_here'
```



### 3. Storing Weather Data

Define models in `weather/models.py`:

```python
# DataStream/models.py
from django.db import models
from django.utils import timezone

class WeatherData(models.Model):
    main = models.CharField(max_length=50)
    temp = models.FloatField()
    feels_like = models.FloatField()
    dt = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-dt']

    def __str__(self):
        return f"{self.main} at {self.dt} - {self.temp}°C"


class DailyWeatherSummary(models.Model):
    date = models.DateField(unique=True)
    avg_temp = models.FloatField()
    max_temp = models.FloatField()
    min_temp = models.FloatField()
    dominant_condition = models.CharField(max_length=50)

    def __str__(self):
        return f"Summary for {self.date} - Avg: {self.avg_temp}°C"
```
### DailyWeatherSummary
![image](https://github.com/user-attachments/assets/ffe527ad-e885-4897-ae8b-044c9a4a0876)
### WeatherData
![image](https://github.com/user-attachments/assets/78a9a39d-fa2e-4948-a19a-bace4df00b3f)

Apply migrations for the new models:

```bash
python manage.py makemigrations
python manage.py migrate
```

---





### 4. Scheduling Data Fetching with Background Tasks

**Create a Task to Fetch Weather Data Regularly:**

In `weather/tasks.py`:

```python
# DataStream/tasks.py
from background_task import background
from .utils import fetch_weather_data, aggregate_daily_weather

@background(schedule=300) # every 5 minutes
def update_weather_data():
    fetch_success = fetch_weather_data()
    if fetch_success:
        aggregate_daily_weather()
```

**Run the Background Task Processor:**

```bash
python manage.py process_tasks
```

**Schedule the Task in Django Shell:**

```bash
python manage.py shell
```

In the shell:

```python
from weather.tasks import update_weather_data
update_weather_data()  # Run every 300 seconds or 5 minutes
```

---

### 5. Admin Setup

Register models in `DataStream/admin.py`:

```python
# weather/admin.py
from django.contrib import admin
from .models import WeatherData, DailyWeatherSummary

@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ('main', 'temp', 'feels_like', 'dt')
    list_filter = ('main', 'dt')
    search_fields = ('main',)

@admin.register(DailyWeatherSummary)
class DailyWeatherSummaryAdmin(admin.ModelAdmin):
    list_display = ('date', 'avg_temp', 'max_temp', 'min_temp', 'dominant_condition')
    list_filter = ('date',)
    search_fields = ('dominant_condition',)
```

**Create Superuser and Access Admin:**

```bash
python manage.py createsuperuser
python manage.py runserver
```

Access the admin interface at `http://127.0.0.1:8000/admin`.

USERNAME: cham
PASSWORD: 1234



---

### Summary of Commands

Here’s a quick reference for the essential commands:

```bash
# 1. Activate virtual environment
source env/bin/activate

# 2. Install dependencies
pip install django requests django-background-tasks

# 3. Apply migrations
python manage.py makemigrations
python manage.py migrate
python manage.py migrate background_task

# 4. Start background task processor
python manage.py process_tasks

# 5. Schedule weather data fetching task in Django shell
python manage.py shell
# Inside shell
from weather.tasks import update_weather_data
update_weather_data(repeat=300)

# 6. Run the Django server
python manage.py runserver
```

