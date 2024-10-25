from django.db import models
from django.utils import timezone

class WeatherData(models.Model):
    main = models.CharField(max_length=50)
    temp = models.FloatField()  # in Celsius
    feels_like = models.FloatField()  # in Celsius
    dt = models.DateTimeField(default=timezone.now)  # timestamp of the update

    class Meta:
        ordering = ['-dt']  # Newest entries first

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
