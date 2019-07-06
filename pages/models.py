from django.db import models
import os
# Create your models here.


class page(models.Model):
    class Meta:
        ordering = ['title']
    title = models.CharField(max_length=42)
    file_name = models.CharField(max_length=42)

    @staticmethod
    def parse():
        result = []

        directory = os.fsencode('static/pages/')

        for file in os.listdir(directory):
            result_file_name = os.fsdecode(file)

            result_title = result_file_name.find('.html')
            if result_title is not -1 and result_file_name is not '.DS_Store':
                result_title = result_file_name[:result_title]
                result_title = ' '.join(result_title.split('_'))
                result_title = ' '.join(result_title.split('-'))

                result.append(page(
                    title=result_title,
                    file_name=result_file_name
                ))

        return result