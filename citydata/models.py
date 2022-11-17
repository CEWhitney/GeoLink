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

    def air(self, user):
        user= user._wrapped if hasattr(user,'_wrapped') else user
        network = Network.objects.get(city=self,owner=user)
        return network.air
    
    def other(self, edge):  #returns city that isn't current city from edge
        if self == edge.city1:
            return edge.city2
        return edge.city1

class Network(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    city = models.ForeignKey(Cities, on_delete=models.CASCADE)
    air = models.BooleanField()

    def initEdges(owner, air_num, miles): #initalize edges for a user with a couple basic parameters. Good starting place for network
        #start by deleting all edges
        edges = Network.edges(owner)
        edges.delete()
        net = Network.objects.filter(owner=owner)
        air = net.filter(air=True)
        for a in air:   #connect all air cities to all other air cities
            ex = air.exclude(city=a.city)
            for e in ex:
                edge = Edge(owner=owner,city1=a.city,city2=e.city,air=True)
                edge.save()
            air = ex
        
        #connect all land cities to air_num nearest air cities
        air = net.filter(air=True)
        land = net.filter(air=False)
        for l in land:
            i =1


        #connect all land cities to all other land cities within range miles

    def delete_edges(self):
        edges = Edge.objects.filter(owner=self.owner)
        for e in edges:
            if self.city == e.city1 or self.city == e.city2:
                e.delete()
    
    def edges(owner):
        return Edge.objects.filter(owner=owner)

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

class Edge(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    city1 = models.ForeignKey(Cities, on_delete=models.CASCADE, related_name='city1')
    city2 = models.ForeignKey(Cities, on_delete=models.CASCADE, related_name='city2')
    air = models.BooleanField()

    def is_edge(c1, c2, user):
        edges = Edge.objects.filter(owner=user)
        for e in edges:
            if (e.city1 == c1 and e.city2 == c2) or (e.city2 == c1 and e.city1 == c2):
                return True
        return False