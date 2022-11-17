import django_tables2 as tables
from citydata.models import Cities, Edge
from django_tables2 import TemplateColumn



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
    edit = TemplateColumn(template_name="columns/edit.html", orderable=False, verbose_name="Edit/View")

    def render_air(self, value, record):
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
    
    add = TemplateColumn(template_name="columns/add.html", orderable=False)

class LinkedTable(tables.Table):
    class Meta:
        model = Cities

        fields = ['city', 'lat', 'lng', 'country', 'population', 'air', 'edit']
        attrs = {"class": "table table-striped table-bordered text-nowrap ",
                 "th": {
                        "width": "10%",
                        "class": "table-light"
                    }
                 }