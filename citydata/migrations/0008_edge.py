# Generated by Django 4.1.3 on 2022-11-14 22:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('citydata', '0007_network_air'),
    ]

    operations = [
        migrations.CreateModel(
            name='Edge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('air', models.BooleanField()),
                ('city1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='city1', to='citydata.cities')),
                ('city2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='city2', to='citydata.cities')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]