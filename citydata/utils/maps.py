import requests
import polyline
import folium

def get_route(pickup_lon, pickup_lat, dropoff_lon, dropoff_lat):
    
    loc = "{},{};{},{}".format(pickup_lon, pickup_lat, dropoff_lon, dropoff_lat)
    url = "http://router.project-osrm.org/route/v1/driving/"
    r = requests.get(url + loc) 
    if r.status_code!= 200:
        return {}
  
    res = r.json()   
    routes = polyline.decode(res['routes'][0]['geometry'])
    start_point = [res['waypoints'][0]['location'][1], res['waypoints'][0]['location'][0]]
    end_point = [res['waypoints'][1]['location'][1], res['waypoints'][1]['location'][0]]
    distance = res['routes'][0]['distance']
    code = res['code']
    duration = res['routes'][0]['duration']

    out = {
           'code':code,
           'route':routes,
           'start_point':start_point,
           'end_point':end_point,
           'distance':distance,
           'duration':duration,
          }

    return out

def get_route_map(cities, route):
    m = folium.Map(min_zoom=1.5, max_bounds=True)
    m.fit_bounds([[-40, -120], [80, 120]])

    for c in cities:
        city_type = '<b>Hub</b>' if c.hub else 'Air: ' + str(c.air)
        info = (
            '<b>' + str(c.city.city) + '</b> <br>' +
            'Population: ' + format(c.city.population, ',d') + '<br>' +
            city_type
            )
        iframe = folium.IFrame(info,width=150, height=100)

        if c.city == route['S'][0]:
            folium.CircleMarker(
                location = [str(c.city.lat), str(c.city.lng)],
                popup = folium.Popup(iframe,max_width=150),
                color = 'green',
            ).add_to(m)
        elif c.city == route['S'][len(route['S'])-1]:
            folium.CircleMarker(
                location = [str(c.city.lat), str(c.city.lng)],
                popup = folium.Popup(iframe,max_width=150),
                color = 'red',
            ).add_to(m)
        elif route['S'].count(c.city) > 0:
            folium.CircleMarker(
                location = [str(c.city.lat), str(c.city.lng)],
                popup = folium.Popup(iframe,max_width=150),
            ).add_to(m)

    for e in route['edge_trace']:
        link_type = 'Type: Air' if e.air else 'Type: Road'
        info = (
            '<b>' + str(e.city1.city) + '</b> to <b>' + str(e.city2.city) + '</b><br>' +
            'Distance: ' + "{:,}".format(e.distance) + ' mi.<br>' +
            'Duration: ' + str(e.duration) + ' hours<br>' +
            link_type
        )
        iframe = folium.IFrame(info,width=200, height=100)
        if e.air:
            folium.PolyLine(
                e.line,
                popup = folium.Popup(iframe,max_width=150)
            ).add_to(m)
        else:
            folium.PolyLine(
                e.line,
                weight=8,
                color='green',
                opacity=0.6,
                popup = folium.Popup(iframe,max_width=150)
            ).add_to(m)

    m=m._repr_html_()

    return m

def get_static_map(cities):
    m = folium.Map(min_zoom=1.5, max_bounds=True)
    m.fit_bounds([[-40, -120], [80, 120]])

    for c in cities:
        city_type = '<b>Hub</b>' if c.hub else 'Air: ' + str(c.air)
        info = (
            '<b>' + str(c.city.city) + '</b> <br>' +
            'Population: ' + format(c.city.population, ',d') + '<br>' +
            city_type
            )
        iframe = folium.IFrame(info,width=150, height=100)
        folium.Marker(
            location = [str(c.city.lat), str(c.city.lng)],
            popup = folium.Popup(iframe,max_width=150)
        ).add_to(m)

    m=m._repr_html_()

    return m

def get_link_map(cities, links):
    m = folium.Map(min_zoom=1.5, max_bounds=True)
    m.fit_bounds([[-40, -120], [80, 120]])

    for c in cities:
        city_type = '<b>Hub</b>' if c.hub else 'Air: ' + str(c.air)
        info = (
            '<b>' + str(c.city.city) + '</b> <br>' +
            'Population: ' + format(c.city.population, ',d') + '<br>' +
            city_type
            )
        iframe = folium.IFrame(info,width=200, height=80)
        folium.Marker(
            location = [str(c.city.lat), str(c.city.lng)],
            popup = folium.Popup(iframe,max_width=200)
        ).add_to(m)

    for l in links:
        points = [[l.city1.lat, l.city1.lng], [l.city2.lat, l.city2.lng]]
        link_type = 'Type: Air' if l.air else 'Type: Road'
        info = (
            '<b>' + str(l.city1.city) + '</b> to <b>' + str(l.city2.city) + '</b><br>' +
            'Distance: ' + "{:,}".format(l.distance) + ' mi.<br>' +
            'Duration: ' + str(l.duration) + ' hours<br>' +
            link_type
            )
        iframe = folium.IFrame(info,width=200, height=100)
        if l.air:
            folium.PolyLine(points, popup = folium.Popup(iframe,max_width=200)).add_to(m)
        else:
            folium.PolyLine(
                l.line,
                weight=8,
                color='green',
                opacity=0.6,
                popup = folium.Popup(iframe,max_width=150)
            ).add_to(m)


    m=m._repr_html_()

    return m