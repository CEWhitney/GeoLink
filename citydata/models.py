from django.db import models
from django.contrib.gis.db import models as geo
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

    def air(self, user): #returns true if network object for current user and this city has air access
        user= user._wrapped if hasattr(user,'_wrapped') else user
        network = Network.objects.get(city=self,owner=user)
        return network.air

class Network(models.Model): #network vertex
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    city = models.ForeignKey(Cities, on_delete=models.CASCADE)
    hub = models.BooleanField()
    air = models.BooleanField()
    
    def delete_edges(self):
        edges = Edge.objects.filter(owner=self.owner)
        for e in edges:
            if self.city == e.city1 or self.city == e.city2:
                e.delete()
    
    def edges(self, owner):
        return list(Edge.objects.filter(city1=self.city,owner=owner) | Edge.objects.filter(city2=self.city,owner=owner))

    def linked(self):   #returns querylist of cities with edges to current city
        city_list = []
        edges = Edge.objects.filter(owner=self.owner,city1=self.city) | Edge.objects.filter(owner=self.owner,city2=self.city)
        for e in edges:
            if (e.city1==self.city):
                city_list.append(e.city2.id)
            else:
                city_list.append(e.city1.id)
        res = Cities.objects.filter(id__in=city_list)
        return res

class Edge(models.Model):   #network edge
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    city1 = models.ForeignKey(Cities, on_delete=models.CASCADE, related_name='city1')
    city2 = models.ForeignKey(Cities, on_delete=models.CASCADE, related_name='city2')
    distance = models.DecimalField(max_digits=7, decimal_places=2)
    duration = models.DecimalField(max_digits=6, decimal_places=2)
    air = models.BooleanField()
    line = geo.LineStringField()
    custom = models.BooleanField()

class Exclusion(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    city1 = models.ForeignKey(Cities, on_delete=models.CASCADE, related_name='excl1')
    city2 = models.ForeignKey(Cities, on_delete=models.CASCADE, related_name='excl2')