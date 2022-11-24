from django.db import models
from django.conf import settings
from geopy import distance

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

    def initEdges(owner, air_num, land_num, miles): #initalize edges for a user with a couple basic parameters. Good starting place for network
        #start by deleting all edges
        edges = Edge.objects.filter(owner=owner)
        edges.delete()

        net = Network.objects.filter(owner=owner)
        hub = net.filter(air=True)
        for h in hub:   #connect all hub cities to all other air cities
            ex = hub.exclude(city=h.city)
            for e in ex:
                loc1 = (h.city.lat, h.city.lng)
                loc2 = (e.city.lat, e.city.lng)
                dist = distance.distance(loc1, loc2).miles
                edge = Edge(owner=owner,city1=h.city,city2=e.city,air=True, custom=False, distance=dist)
                edge.save()
            hub = ex
        
        #connect all land cities to air_num nearest air cities

        #connect all land cities to all other land cities within range miles
    
    def delete_edges(self):
        edges = Edge.objects.filter(owner=self.owner)
        for e in edges:
            if self.city == e.city1 or self.city == e.city2:
                e.delete()
    
    def edges(self, owner):
        return Edge.objects.filter(city1=self.city,owner=owner) | Edge.objects.filter(city2=self.city,owner=owner)

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
    air = models.BooleanField()
    custom = models.BooleanField()

class Exclusion(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    city1 = models.ForeignKey(Cities, on_delete=models.CASCADE, related_name='excl1')
    city2 = models.ForeignKey(Cities, on_delete=models.CASCADE, related_name='excl2')