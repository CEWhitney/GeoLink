import django_tables2 as tables
from citydata.models import Cities
from django_tables2 import TemplateColumn



class CitiesTable(tables.Table):
    class Meta:
        model = Cities

        fields = ['city', 'lat', 'lng', 'country', 'population', 'edit']
        attrs = {"class": "table table-striped table-bordered text-nowrap ",
                 "th": {
                        "width": "10%",
                        "class": "table-light"
                    }
                 }
    
    lat = tables.Column(verbose_name="Latitude")
    lng = tables.Column(verbose_name="Longitude")
    edit = TemplateColumn(template_name="columns/edit.html", orderable=False, verbose_name="Edit/View")

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