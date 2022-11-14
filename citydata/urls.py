from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('manage/', views.ManageView.as_view(), name='manage'),
    path('routing/', views.routing, name='routing'),
    path('register', views.register_request, name='register'),
]