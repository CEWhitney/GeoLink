from django.shortcuts import render, redirect
from .models import Cities, Network, Edge, Exclusion
from .utils.forms import PageForm, InitForm
from .utils.tables import CitiesTable, AllCitiesTable, LinkedTable
from .utils.maps import get_static_map, get_route_map, get_link_map
from .utils.model_utils import initEdges, dijkstra
import django_tables2 as tables
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormMixin
from django.views.generic.base import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages

# Create your views here.
        
def index(request): #home page
    if request.user.is_authenticated:
        cities = Network.objects.filter(owner=request.user)
    else:
        cities = Network.objects.all()
    
    cities_list = list(cities)

    #initEdges(request.user, 1, 1, 74)

    my_map = get_static_map(cities_list)

    context = {
        'num_cities': cities.count(),
        'my_map' : my_map
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

class EditView(tables.SingleTableView): #edit page for single city
    queryset = Cities.objects.all()

    table_class = LinkedTable

    template_name='ManageViews/city_edit.html'

    def get_queryset(self):
        city = Cities.objects.get(id=self.request.GET.get('city', ''))
        return Network.objects.get(city=city, owner=self.request.user).linked()
        

    def get_context_data(self, **kwargs):
        context = super(EditView, self).get_context_data(**kwargs)
        city = Cities.objects.get(id=self.request.GET.get('city', ''))
        net = Network.objects.get(city=city, owner=self.request.user)

        context['city'] = city
        context['net'] = net

        return context

class ConnectView(TemplateView, FormMixin):
    template_name = "ManageViews/Connections/init.html"

    form_class = InitForm

    def get_context_data(self, **kwargs):
        context = super(ConnectView, self).get_context_data(**kwargs)
        cities = Network.objects.filter(owner=self.request.user)
        edges = Edge.objects.filter(owner=self.request.user)
        edge_list = list(edges)
        cities_list = list(cities)

        my_map = get_link_map(cities_list, edge_list)

        context['my_map'] = my_map

        return context

    def post(self,request): #form submit, adds form values to url params
        form = InitForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/citydata/init?air='+form.cleaned_data['air_num']+'&land='+form.cleaned_data['land_num']+'&range='+form.cleaned_data['land_range'])
        return HttpResponseRedirect('/citydata/manage/connections/')

class AddEdgeView(TemplateView):
    template_name = "ManageViews/Connections/add.html"

class CustomEdgeView(tables.SingleTableView):
    template_name = "ManageViews/Connections/custom.html"

    table_class = CitiesTable

    def get_queryset(self):
        return Edge.objects.filter(owner=self.request.user, custom=True)

class ExclusionsView(tables.SingleTableView):
    template_name = "ManageViews/Connections/exclusions.html"

    table_class = CitiesTable

    def get_queryset(self):
        return Exclusion.objects.filter(owner=self.request.user)


class RoutingView(TemplateView):
    template_name = 'routing.html'

    def get_context_data(self, **kwargs):
        context = super(RoutingView, self).get_context_data(**kwargs)

        networks = Network.objects.filter(owner=self.request.user)
        cities = []
        for n in networks:
            cities.append(n.city)
        context['cities'] = cities

        return context
    
    def post(self, request):
        form = request.POST
        city1 = form.get('city1_select', "")
        city2 = form.get('city2_select', "")
        priority = form.get('priority', "")
        return HttpResponseRedirect('/citydata/routing/result?1='+city1+"&2="+city2+"&p="+priority)
    

class RoutingResultView(TemplateView):
    template_name='routing_result.html'

    def get_context_data(self, **kwargs):
        context = super(RoutingResultView, self).get_context_data(**kwargs)
        city1 = Cities.objects.get(id=int(self.request.GET['1']))
        city2 = Cities.objects.get(id=int(self.request.GET['2']))
        priority = self.request.GET['p']
        cities_list = list(Network.objects.filter(owner=self.request.user))
        path = dijkstra(self.request.user, priority, city1, city2)
        my_map = get_route_map(cities_list, path)
        edges = path['edge_trace']
        dist = []
        time = []
        travel_type = []
        for e in edges:
            dist.append(e.distance)
            time.append(e.duration)
            if e.air:
                travel_type.append("Air")
            else:
                travel_type.append("Road")
        total_dist = sum(dist)
        total_time = sum(time)

        
        context['my_map'] = my_map
        context['edges'] = edges
        context['city1'] = city1.city
        context['city2'] = city2.city
        context['dist'] = dist
        context['time'] = time
        context['path'] = path['S']
        context['travel_type'] = travel_type
        context['total_dist'] = total_dist
        context['total_time'] = total_time


        return context

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

    network = Network(owner=user, city=city, air=request.GET['air'], hub=request.GET['hub'])
    network.save()

    return HttpResponseRedirect('/citydata/manage/add/')

def del_request(request): #delete city from network and redirect back to manage view
    user = request.user
    city = Cities.objects.get(id=request.GET['city'])

    network = Network.objects.get(owner=user,city=city)
    network.delete_edges()
    network.delete()

    return HttpResponseRedirect('/citydata/manage/')

def toggle_request(request): #toggle air access of network and redirect back to edit view
    city = Cities.objects.get(id=request.GET['city'])
    network = Network.objects.get(city=city, owner=request.user)
    attr = request.GET['attr']
    if attr == 'hub':
        network.hub = not network.hub
        network.save()
        return HttpResponseRedirect('/citydata/manage/edit/?city=' + str(network.city.id))

    if (network.air):
        edges = network.edges(request.user)
        for e in edges:
            e.air = False
            e.save()

    network.air = not network.air
    network.save()

    return HttpResponseRedirect('/citydata/manage/edit/?city=' + str(network.city.id))

def init_request(request):
    initEdges(request.user, request.GET['air'], request.GET['land'], request.GET['range'])

    return HttpResponseRedirect('/citydata/manage/connections/')

def credit_view(request):
    return render(request=request, template_name="attribution.html/")

def guide_view(request):
    return render(request=request, template_name='guide.html/')