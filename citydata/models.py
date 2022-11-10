from django.db import models

# Create your models here.

class Cities(models.Model):
    city = models.TextField()
    lat = models.DecimalField(max_digits=7, decimal_places=4)
    lng = models.DecimalField(max_digits=7, decimal_places=4)
    country = models.TextField()
    population = models.IntegerField()
    id = models.BigIntegerField(primary_key=True)

    class Meta:
        ordering = ['-population']
        db_table = 'cities'