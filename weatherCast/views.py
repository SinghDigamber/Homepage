from django.views.generic import ListView
from .models import weatherCast

class weatherCastView(ListView):
    model = weatherCast
    template_name = "weatherCast/index.html"
    context_object_name = "fromView"

    def get_queryset(self):
        # constants
        page_title = "Погода"

        # calculations
        json = weatherCast.download_weather_forecast()

        result_forecast = weatherCast.parse_json_weather(json)
        result_summary = weatherCast.parse_json_weather_summary(json)

        temp_min = min(forecast.temp for forecast in result_forecast)
        temp_max = max(forecast.temp for forecast in result_forecast)

        # results
        return {
            'page': {
                'title': page_title,
                'temp_min': temp_min,
                'temp_max': temp_max,
            },
            'summary': result_summary,
            'forecast': result_forecast,
        }
