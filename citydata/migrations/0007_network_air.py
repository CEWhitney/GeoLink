# Generated by Django 4.1.3 on 2022-11-14 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citydata', '0006_network'),
    ]

    operations = [
        migrations.AddField(
            model_name='network',
            name='air',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
