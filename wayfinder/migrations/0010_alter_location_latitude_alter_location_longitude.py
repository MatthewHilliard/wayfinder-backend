# Generated by Django 5.1.3 on 2024-11-28 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wayfinder', '0009_location_region'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
