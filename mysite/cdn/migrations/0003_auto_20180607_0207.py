# Generated by Django 2.0.6 on 2018-06-07 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cdn', '0002_ysten'),
    ]

    operations = [
        migrations.AddField(
            model_name='washu',
            name='c_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='ysten',
            name='c_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
