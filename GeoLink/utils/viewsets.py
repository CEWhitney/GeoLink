from rest_framework import viewsets, routers
from django.contrib.auth.models import User
from citydata.models import Cities, Network, Edge
from citydata.utils.serializers import UserSerializer, CitySerializer, NetworkSerializer, EdgeSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CityViewSet(viewsets.ModelViewSet):
    queryset = Cities.objects.all()
    serializer_class = CitySerializer

class NetworkViewSet(viewsets.ModelViewSet):
    queryset = Network.objects.all()
    serializer_class = NetworkSerializer

class EdgeViewSet(viewsets.ModelViewSet):
    queryset = Edge.objects.all()
    serializer_class = EdgeSerializer

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'cities', CityViewSet)
router.register(r'networks', NetworkViewSet)
router.register(r'edges', EdgeViewSet)