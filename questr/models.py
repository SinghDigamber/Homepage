from django.db import models
# Create your models here.


class quest(models.Model):
    title = models.CharField(max_length=42)
    description = models.CharField(max_length=420)
