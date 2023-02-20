# Generated by Django 4.1.3 on 2022-11-18 00:04

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('citydata', '0010_edge_custom_exclusion'),
    ]

    operations = [
        migrations.AddField(
            model_name='edge',
            name='distance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
            preserve_default=False,
        ),
    ]
