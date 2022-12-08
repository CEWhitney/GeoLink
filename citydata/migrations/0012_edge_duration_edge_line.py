# Generated by Django 4.1.3 on 2022-12-07 22:11

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citydata', '0011_edge_distance'),
    ]

    operations = [
        migrations.AddField(
            model_name='edge',
            name='duration',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='edge',
            name='line',
            field=django.contrib.gis.db.models.fields.LineStringField(default=(0, 0), srid=4326),
            preserve_default=False,
        ),
    ]