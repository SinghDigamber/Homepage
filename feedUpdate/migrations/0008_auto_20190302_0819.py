# Generated by Django 2.0.3 on 2019-03-02 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedUpdate', '0007_auto_20190225_2050'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feed',
            options={'ordering': ['title']},
        ),
    ]
