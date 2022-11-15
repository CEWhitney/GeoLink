from django.shortcuts import render, redirect
from .models import Cities
from .models import Network
from .utils.forms import PageForm
from .utils.tables import CitiesTable, AllCitiesTable
import django_tables2 as tables
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormMixin
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages

# Create your views here.
        
def index(request): #home page
    if request.user.is_authenticated:
        num_cities = Network.objects.filter(owner=request.user).count()
    else:
        num_cities = Network.objects.all()

    context = {
        'num_cities': num_cities
    }

    return render(request, 'index.html', context = context)

class ManageView(tables.SingleTableView, FormMixin): #list cities in network
    table_class = CitiesTable
    queryset = Cities.objects.all()

    template_name = 'ManageViews/manage_read.html'
    
    form_class = PageForm
    success_url = 'success'

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated: #get list of cities by user network
            user = self.request.user
            net = Network.objects.filter(owner=user).values_list('city',flat=True)
            qs = qs.filter(id__in=net)

        return qs.filter(city__icontains=self.request.GET.get('search', '')) | qs.filter(country__icontains=self.request.GET.get('search', ''))


    def post(self,request): #form submit, adds form values to url params
        form = PageForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/citydata/manage/?page='+form.cleaned_data['new_page']+'&search='+form.cleaned_data['search_query'])
        return HttpResponseRedirect('/citydata/manage/')

class AddView(tables.SingleTableView, FormMixin):
    table_class = AllCitiesTable
    queryset = Cities.objects.all()

    template_name = 'ManageViews/manage_add.html'
    
    form_class = PageForm
    success_url = 'success'

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated: #get list of cities EXCLUDING those already in current user's network
            user = self.request.user
            net = Network.objects.filter(owner=user).values_list('city',flat=True)
            qs = qs.exclude(id__in=net)

        return qs.filter(city__icontains=self.request.GET.get('search', '')) | qs.filter(country__icontains=self.request.GET.get('search', ''))

    def post(self,request): #form submit, adds form values to url params
        form = PageForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/citydata/manage/add/?page='+form.cleaned_data['new_page']+'&search='+form.cleaned_data['search_query'])
        return HttpResponseRedirect('/citydata/manage/add/')

class EditView(View, tables.MultiTableMixin):
    table_class = CitiesTable
    queryset = Cities.objects.all()

    template_name = 'ManageViews/manage_read.html'

    def get(self, request):
        try:    #This wont ever normally throw an exception but this handles someone manually messing with the url
            city = Cities.objects.get(id=request.GET.get('city', ''))
        except Cities.DoesNotExist:
            return HttpResponseRedirect('/citydata/manage/')
        except ValueError:
            return HttpResponseRedirect('/citydata/manage/')
        context = {
            'city': city,
        }
        return render(request, 'ManageViews/city_edit.html', context = context)

def manage_edges(request):

    return render(request, 'ManageViews/manage_edges.html')

def routing(request):

    return render(request, 'routing.html')

def register_request(request): #registration page
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("home")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = UserCreationForm()
	return render (request=request, template_name="registration/register.html", context={"register_form":form})

def add_request(request): #add city to network and redirect back to add view
    user = request.user
    city = Cities.objects.get(id=request.GET['city'])

    network = Network(owner=user, city=city, air=request.GET['air'])
    network.save()

    return HttpResponseRedirect('/citydata/manage/add/')

def del_request(request): #delete city from network and redirect back to manage view
    user = request.user
    city = Cities.objects.get(id=request.GET['city'])

    network = Network.objects.get(owner=user,city=city)
    network.delete_edges()
    network.delete()

    return HttpResponseRedirect('/citydata/manage/')