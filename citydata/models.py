from django.db import models
from django.conf import settings

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

    def linked(self):
        city_list = []
        cities = Cities.objects.all()
        for c in cities:
            if Edge.is_edge(self.id, c.id):
                city_list.append(c.id)
        cities = cities.filter(id__in=city_list)
        return cities
    
    def other(self, edge):
        if self == edge.city1:
            return edge.city2
        return edge.city1

class Network(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    city = models.ForeignKey(Cities, on_delete=models.CASCADE)
    air = models.BooleanField()

    def delete_edges(self):
        edges = Edge.objects.filter(owner=self.owner)
        for e in edges:
            if self.city == e.city1 or self.city == e.city2:
                e.delete()

class Edge(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    city1 = models.ForeignKey(Cities, on_delete=models.CASCADE, related_name='city1')
    city2 = models.ForeignKey(Cities, on_delete=models.CASCADE, related_name='city2')
    air = models.BooleanField()

    def is_edge(c1, c2):
        edges = Edge.objects.all()
        for e in edges:
            if (e.city1 == c1 and e.city2 == c2) or (e.city2 == c1 and e.city1 == c2):
                return True
        return False