import django_tables2 as tables
from citydata.models import Cities, Edge

class CitiesTable(tables.Table):
    class Meta:
        model = Cities

        fields = ['city', 'lat', 'lng', 'country', 'population', 'air', 'edit']
        attrs = {"class": "table table-striped table-bordered text-nowrap ",
                 "th": {
                        "width": "10%",
                        "class": "table-light"
                    }
                 }
    
    lat = tables.Column(verbose_name="Latitude")
    lng = tables.Column(verbose_name="Longitude")
    air = tables.Column(empty_values=(), orderable=False, verbose_name="Air Access")
    edit = tables.TemplateColumn(template_name="columns/edit.html", orderable=False, verbose_name="Edit/View")

    def render_air(self, record):
        city = Cities.objects.get(id=record.id)
        if city.air(self.request.user) == True:
            return 'Yes'
        return 'No'

class AllCitiesTable(tables.Table):
    class Meta:
        model = Cities

        fields = ['city', 'lat', 'lng', 'country', 'population', 'add']
        attrs = {"class": "table table-striped table-bordered text-nowrap ",
                 "th": {
                        "width": "10%",
                        "class": "table-light"
                    }
                 }
    
    lat = tables.Column(verbose_name="Latitude")
    lng = tables.Column(verbose_name="Longitude")
    add = tables.TemplateColumn(template_name="columns/add.html", orderable=False)

class LinkedTable(tables.Table):
    class Meta:
        model = Cities

        fields = ['city', 'lat', 'lng', 'country', 'population', 'distance', 'air']
        attrs = {"class": "table table-striped table-bordered text-nowrap ",
                 "th": {
                        "width": "10%",
                        "class": "table-light"
                    }
                 }

    lat = tables.Column(verbose_name="Latitude")
    lng = tables.Column(verbose_name="Longitude")
    distance = tables.Column(empty_values=(), orderable=False, verbose_name="Travel Distance")
    air = tables.Column(empty_values=(), orderable=False, verbose_name="Air Route")

    def render_distance(self,record):
        city1 = Cities.objects.get(id=self.request.GET['city'])
        city2 = Cities.objects.get(id=record.id)
        
        edge = Edge.objects.filter(city1=city1,city2=city2,owner=self.request.user) | Edge.objects.filter(city1=city2,city2=city1,owner=self.request.user)

        return str(edge[0].distance) + ' mi.'

    def render_air(self, record):
        city1 = Cities.objects.get(id=self.request.GET['city'])
        city2 = Cities.objects.get(id=record.id)
        
        edge = Edge.objects.filter(city1=city1,city2=city2,owner=self.request.user) | Edge.objects.filter(city1=city2,city2=city1,owner=self.request.user)

        if edge[0].air == True:
            return 'Yes'
        return 'No'