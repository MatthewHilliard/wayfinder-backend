# Generated by Django 5.1.3 on 2024-11-29 02:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wayfinder', '0010_alter_location_latitude_alter_location_longitude'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='user_id',
            new_name='id',
        ),
    ]
