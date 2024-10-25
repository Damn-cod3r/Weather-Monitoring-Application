from django.contrib import admin
from .models import WeatherData, DailyWeatherSummary

@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ('main', 'temp', 'feels_like', 'dt')
    list_filter = ('main', 'dt')
    search_fields = ('main',)
    ordering = ('-dt',)

@admin.register(DailyWeatherSummary)
class DailyWeatherSummaryAdmin(admin.ModelAdmin):
    list_display = ('date', 'avg_temp', 'max_temp', 'min_temp', 'dominant_condition')
    list_filter = ('date',)
    search_fields = ('dominant_condition',)
    ordering = ('-date',)
