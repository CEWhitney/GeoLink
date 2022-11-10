from django.shortcuts import render
from .models import Cities
from .utils.forms import PageForm
from .utils.forms import SearchForm
import django_tables2 as tables
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormMixin

# Create your views here.

class CitiesTable(tables.Table):
    class Meta:
        model = Cities
        attrs = {"class": "table table-striped table-bordered text-nowrap",
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

class ManageView(tables.SingleTableView, FormMixin):
    table_class = CitiesTable
    queryset = Cities.objects.all()

    template_name = 'ManageViews/manage_read.html'
    
    form_class = PageForm
    success_url = 'success'

    def get(self, request, *args, **kwargs):
        context = {'pageform': PageForm(), 'searchform': SearchForm()}
        return self.render_to_response('ManageView/manage_read.html', context)

    def post(self,request):
        form = PageForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/citydata/manage/?page='+form.cleaned_data['new_page'])
        return HttpResponseRedirect('/citydata/manage/')

def routing(request):

    return render(request, 'routing.html')

def new_page(request):
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/citydata/manage/?page='+form.new_page)
    else :
        form = PageForm()
    
    return HttpResponseRedirect('/citydata/manage/')