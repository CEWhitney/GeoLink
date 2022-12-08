from citydata.models import Cities, Network, Edge
from django.contrib.gis.geos import LineString
from geopy import distance
from citydata.utils.maps import get_route

def initEdges(owner, air_num, land_num, miles): #initalize edges for a user with a couple basic parameters. Good starting place for network
        if air_num == '':
            air_num = 3
        if land_num == '':
            land_num = 2
        if miles == '':
            miles = 75

        #start by deleting all edges
        edges = Edge.objects.filter(owner=owner)
        edges.delete()

        net = Network.objects.filter(owner=owner)
        hub = net.filter(hub=True)
        for h in hub:   #connect all hub cities to all other hub cities
            ex = hub.exclude(city=h.city)
            for e in ex:
                loc1 = (h.city.lat, h.city.lng)
                loc2 = (e.city.lat, e.city.lng)
                dist = distance.distance(loc1, loc2).miles
                edge = Edge(owner=owner,city1=h.city,city2=e.city,air=True, custom=False, distance=dist, line=LineString((h.city.lat,h.city.lng), (e.city.lat,e.city.lng)))
                edge.duration = edge.distance / 500
                edge.save()
            hub = ex

        #connect all air cities to air_num nearest non land cities
        air = net.filter(air=True, hub=False)
        for a in air:
            ex = net.filter(air=True).exclude(city=a.city)
            ex = sorted(ex, key= lambda e: distance.distance((a.city.lat, a.city.lng), (e.city.lat, e.city.lng)))
            edges = Edge.objects.filter(owner=owner)
            current_links = edges.filter(city1=a.city) | edges.filter(city2=a.city)
            air_range = int(air_num) - current_links.count()
            for i in range(air_range+1):
                edge = Edge(owner=owner, city1=a.city, city2=ex[i].city, air=True, custom=False, distance=distance.distance((a.city.lat, a.city.lng), 
                        (ex[i].city.lat, ex[i].city.lng)).miles, line=LineString((a.city.lat,a.city.lng), (ex[i].city.lat,ex[i].city.lng)))
                edge.duration = edge.distance / 500
                edge.save()
        
        #connect all land cities to land_num nearest air cities
        land = net.filter(air=False, hub=False)
        air = net.filter(air=True)
        for l in land:
            air = sorted(air, key= lambda a: distance.distance((l.city.lat, l.city.lng), (a.city.lat, a.city.lng)))
            edges = Edge.objects.filter(owner=owner)
            current_links = edges.filter(city1=l.city) | edges.filter(city2=l.city)
            land_range = int(land_num) - current_links.count()
            for i in range(land_range):
                edge = Edge(owner=owner, city1=l.city, city2=air[i].city, air=False, custom=False, distance=1, line=LineString((0,0), (1,1)))
                route = get_route(l.city.lng, l.city.lat, air[i].city.lng, air[i].city.lat)
                if len(route) > 0:
                    if route['code'] != 'NoRoute':
                        edge.distance = round(route['distance']/1609, 2)
                        edge.line = LineString(route['route'])
                        edge.duration = route['duration']/3600
                        edge.save()
                else:
                    land_range += 1
                    if i == len(air):
                        break

        #connect all land cities to all other land cities within range miles
        land = net.filter(air=False, hub=False)
        for l in land:
            ex = land.exclude(city=l.city)
            ex = sorted(ex, key= lambda e: distance.distance((l.city.lat, l.city.lng), (e.city.lat, e.city.lng)))
            for e in ex:
                if distance.distance((l.city.lat, l.city.lng), (e.city.lat, e.city.lng)) > land_range:
                    break
                edge = Edge(owner=owner, city1=l.city, city2=e.city, air=False, custom=False, distance=1, line=LineString((0,0), (1,1)))
                route = get_route(l.city.lng, l.city.lat, air[i].city.lng, air[i].city.lat)
                if route['code'] != 'NoRoute':
                    edge.distance = round(route['distance']/1609, 2)
                    edge.line = LineString(route['route'])
                    edge.duration = route['duration']/3600
                    edge.save()
            land = land.exclude(city=l.city)

def dijkstra(owner, mode, city1, city2):
    vertices = list(Network.objects.filter(owner=owner))
    dist = [999999] * len(vertices)
    prev = [None] * len(vertices)
    queue = []
    for i in range(len(vertices)):
        if vertices[i].city == city1:
            source = i
        if vertices[i].city == city2:
            sink = i
        queue.append(i)
    
    dist[source] = 0

    while len(queue) > 0:
        u = queue[0]
        for q in queue:
            if dist[q] < dist[u]:
                u = q
        if u == sink:
            S = []
            edge_trace = []
            if prev[u] != None or u == source:
                while u != None:
                    S.insert(0,vertices[u].city)
                    edges = Edge.objects.filter(owner=owner)
                    if prev[u] != None:
                        edge_trace.insert(0,(edges.filter(city1=vertices[u].city,city2=vertices[prev[u]].city) | edges.filter(city2=vertices[u].city,city1=vertices[prev[u]].city))[0])
                    u = prev[u]
            result = {
                'S': S,
                'edge_trace': edge_trace,
                'dist': dist,
                'prev': prev,
                'queue': queue,
            }
            return result
        queue.remove(u)

        edges = vertices[u].edges(owner)
        connected = []
        for e in edges:
            if e.city1 == vertices[u].city:
                connected.append(e.city2)
            else:
                connected.append(e.city1)
        current = []
        for q in queue:
            current.append(vertices[q].city)
        
        connected = list(set(connected).intersection(set(current)))
        for v in connected:
            edge = (Edge.objects.filter(city1=vertices[u].city,city2=v) | Edge.objects.filter(city1=v,city2=vertices[u].city))[0]
            alt = dist[u] + edge.distance if mode == 'distance' else dist[u] + edge.duration
            net = Network.objects.get(owner=owner,city=v)
            if alt < dist[vertices.index(net)]:
                dist[vertices.index(net)] = alt
                prev[vertices.index(net)] = u
        
    return 'fail'
