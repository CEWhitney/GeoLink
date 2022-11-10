from django.shortcuts import render
from .models import Cities
from django.views import generic
from .utils import forms
import django_tables2 as tables

# Create your views here.

class CitiesTable(tables.Table):
    class Meta:
        model = Cities
        attrs = {"class": "table table-striped table-bordered w-auto",
                 "th": {
                        "width": "10%"
                    }
                 }

def index(request):
    num_cities = Cities.objects.count()

    context = {
        'num_cities': num_cities

    }

    return render(request, 'index.html', context = context)

class ManageView(tables.SingleTableView):
    table_class = CitiesTable

    queryset = Cities.objects.all()

    template_name = 'ManageViews/manage_read.html'



def routing(request):

    return render(request, 'routing.html')