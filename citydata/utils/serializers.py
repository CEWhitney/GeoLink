from rest_framework import serializers
from django.contrib.auth.models import User
from citydata.models import Cities, Network, Edge

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'is_staff']

class CitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cities
        fields = '__all__'

class NetworkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Network
        fields = '__all__'

class EdgeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Edge
        fields = '__all__'