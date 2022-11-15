from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('manage/add/', views.AddView.as_view(), name='manage_add'),
    path('manage/edges/', views.manage_edges, name='edges'),
    path('manage/', views.ManageView.as_view(), name='manage'),
    path('routing/', views.routing, name='routing'),
    path('register', views.register_request, name='register'),
    path('manage/edit', views.EditView.as_view(), name='edit'),
    path('add', views.add_request, name='add'),
    path('delete', views.del_request, name='delete'),
]