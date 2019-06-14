from django.db import models
# from bs4 import BeautifulSoup, SoupStrainer
import requests
import json
from datetime import datetime
# Create your models here.

# TODO: move project to actual database


class weatherCast(models.Model):
    location = "50.042836,36.352614"
    flags = "?lang=ru&units=si"
    baseURL = "https://api.darksky.net/forecast/d372cd235cbdf209f6a075fbf35f262d/"+location+flags

    # download weather forecast
    @staticmethod
    def download_weather_forecast():
        request = requests.get(weatherCast.baseURL).json()

        return request

    # parse example json
    @staticmethod
    def open_weather_forecast_example():
        # read file
        with open('weatherCast/example.json', 'r') as myfile:
            data = myfile.read()

        # parse file
        obj = json.loads(data)

        return obj

    # open weather forecast example file
    @staticmethod
    def parse_json_weather(json):
        # parse weather
        result = []
        #result.append("---- Current Weather: ----")
        #result.append(json['currently']['summary'])
        result.append(weather_point(
            summary=json['currently']['summary'],
            temp=json['currently']['temperature'],
            temp_type="R",
            cloudCover=float(json['currently']['cloudCover']),
            datetime=datetime.fromtimestamp(json['currently']['time']),
            point_type="N"
        ))
        result.append(weather_point(
            summary=json['currently']['summary'],
            temp=json['currently']['apparentTemperature'],
            temp_type="F",
            cloudCover=float(json['currently']['cloudCover']),
            datetime=datetime.fromtimestamp(json['currently']['time']),
            point_type="N"
        ))

        #result.append("---- Hourly Forecast: ----")
        #result.append(json['hourly']['summary'])
        for data in json['hourly']['data']:
            result.append(weather_point(
                summary=data['summary'],
                temp=data['temperature'],
                temp_type="R",
                cloudCover=float(data['cloudCover']),
                datetime=datetime.fromtimestamp(data['time']),
                point_type="H"
            ))
            result.append(weather_point(
                summary=data['summary'],
                temp=data['apparentTemperature'],
                temp_type="F",
                cloudCover=float(data['cloudCover']),
                datetime=datetime.fromtimestamp(data['time']),
                point_type="H"
            ))

        #result.append("---- Daily Forecast: ----")
        #result.append(json['daily']['summary'])
        for data in json['daily']['data']:
            result.append(weather_point(
                summary=data['summary'],
                temp=data['temperatureHigh'],
                temp_type="R",
                cloudCover=float(data['cloudCover']),
                datetime=datetime.fromtimestamp(data['temperatureHighTime']),
                point_type="D"
            ))
            result.append(weather_point(
                summary=data['summary'],
                temp=data['temperatureLow'],
                temp_type="R",
                cloudCover=float(data['cloudCover']),
                datetime=datetime.fromtimestamp(data['temperatureLowTime']),
                point_type="D"
            ))
            result.append(weather_point(
                summary=data['summary'],
                temp=data['temperatureMin'],
                temp_type="R",
                cloudCover=float(data['cloudCover']),
                datetime=datetime.fromtimestamp(data['temperatureMinTime']),
                point_type="D"
            ))
            result.append(weather_point(
                summary=data['summary'],
                temp=data['temperatureMax'],
                temp_type="R",
                cloudCover=float(data['cloudCover']),
                datetime=datetime.fromtimestamp(data['temperatureMaxTime']),
                point_type="D"
            ))
            result.append(weather_point(
                summary=data['summary'],
                temp=data['apparentTemperatureHigh'],
                temp_type="F",
                cloudCover=float(data['cloudCover']),
                datetime=datetime.fromtimestamp(data['apparentTemperatureHighTime']),
                point_type="D"
            ))
            result.append(weather_point(
                summary=data['summary'],
                temp=data['apparentTemperatureLow'],
                temp_type="F",
                cloudCover=float(data['cloudCover']),
                datetime=datetime.fromtimestamp(data['apparentTemperatureLowTime']),
                point_type="D"
            ))
            result.append(weather_point(
                summary=data['summary'],
                temp=data['apparentTemperatureMin'],
                temp_type="F",
                cloudCover=float(data['cloudCover']),
                datetime=datetime.fromtimestamp(data['apparentTemperatureMinTime']),
                point_type="D"
            ))
            result.append(weather_point(
                summary=data['summary'],
                temp=data['apparentTemperatureMax'],
                temp_type="F",
                cloudCover=float(data['cloudCover']),
                datetime=datetime.fromtimestamp(data['apparentTemperatureMaxTime']),
                point_type="D"
            ))

        return result

    def parse_json_weather_summary(json):
        result = {
            'now': json['currently']['summary'],
            'day': json['hourly']['summary'],
            'week': json['daily']['summary']
        }

        return result

    def parse_json_weather_now_summary_compiled(json):
        result_summary = json['currently']['summary']
        result_summary = result_summary.lower()

        result_temp = json['currently']['apparentTemperature']
        result_temp = round(result_temp, 0)
        result_temp = int(result_temp)
        result_temp = str(result_temp)

        return {
            'summary': result_summary,
            'temp': result_temp,
        }


class weather_point(models.Model):
    class Meta:
        ordering = ['-datetime']
    summary = models.CharField(max_length=140)
    temp = models.FloatField()
    TEMP_TYPES = (
        ('R', 'Real'),
        ('F', 'Feels'),
    )
    temp_type = models.CharField(max_length=1, choices=TEMP_TYPES)
    cloudCover = models.FloatField()
    datetime = models.DateTimeField()
    POINT_TYPES = (
        ('N', 'Now'),
        ('H', 'Hourly'),
        ('D', 'Daily'),
    )
    point_type = models.CharField(max_length=1, choices=POINT_TYPES)

    def __str__(self):
        result=""
        result += "sum: "+self.summary+" | "
        result += "temp: "+str(self.temp)+" | "
        result += "temp_type: "+self.temp_type+" | "
        result += "cloudCover: "+str(self.cloudCover)+" | "
        result += "datetime: "+str(self.datetime)+" | "
        result += "point_type: "+self.point_type

        return result