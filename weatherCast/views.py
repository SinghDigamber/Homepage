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

        json_hourly_feels = []

        json_cloudCover_hourly = []

        for each in result_forecast:
            if each.point_type == 'H' and each.temp_type == 'F':
                json_hourly_feels.append(round(each.temp, 2))
            elif each.point_type == 'H':
                json_cloudCover_hourly.append(int(each.cloudCover*100))

        # results
        return {
            'page': {
                'title': page_title,
            },
            'summary': result_summary,
            'forecast': result_forecast,
            'json_hourly_feels': str(json_hourly_feels[:25]),
            'json_cloudCover_hourly': str(json_cloudCover_hourly[:25]),
        }
