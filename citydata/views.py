from django.shortcuts import render
from .models import Cities
from .utils.forms import PageForm
import django_tables2 as tables
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormMixin
from django_filters.views import FilterView

# Create your views here.

class CitiesTable(tables.Table):
    class Meta:
        model = Cities
        attrs = {"class": "table table-striped table-bordered text-nowrap ",
                 "th": {
                        "width": "10%",
                        "class": "table-light"
                    }
                 }
    
def index(request):
    num_cities = Cities.objects.count()

    context = {
        'num_cities': num_cities

    }

    return render(request, 'index.html', context = context)

class ManageView(tables.SingleTableView, FormMixin, FilterView):
    table_class = CitiesTable
    queryset = Cities.objects.all()

    template_name = 'ManageViews/manage_read.html'
    
    form_class = PageForm
    success_url = 'success'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(city__icontains=self.request.GET.get('search', '')) | qs.filter(country__icontains=self.request.GET.get('search', ''))


    def post(self,request):
        form = PageForm(request.POST)
        if form.is_valid():
            queryset = Cities.objects.all().filter(city__icontains=form.cleaned_data['search_query'])
            return HttpResponseRedirect('/citydata/manage/?page='+form.cleaned_data['new_page']+'&search='+form.cleaned_data['search_query'])
        return HttpResponseRedirect('/citydata/manage/')

def routing(request):

    return render(request, 'routing.html')
