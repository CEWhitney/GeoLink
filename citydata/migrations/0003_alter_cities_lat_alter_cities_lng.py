# Generated by Django 4.1.3 on 2022-11-11 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citydata', '0002_alter_cities_options_alter_cities_lat_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cities',
            name='lat',
            field=models.DecimalField(decimal_places=4, max_digits=7),
        ),
        migrations.AlterField(
            model_name='cities',
            name='lng',
            field=models.DecimalField(decimal_places=4, max_digits=7),
        ),
    ]
