from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('attributions/', views.credit_view, name='credits'),
    path('guide/', views.guide_view, name = 'guide'),
    path('manage/add/', views.AddView.as_view(), name='manage_add'),
    path('manage/connections/', views.ConnectView.as_view(), name='edges'),
    path('manage/connections/add/', views.AddEdgeView.as_view(), name='add_edges'),
    path('manage/connections/custom/', views.CustomEdgeView.as_view(), name='custom'),
    path('manage/connections/exclusions/', views.ExclusionsView.as_view(), name='exclusions'),
    path('manage/', views.ManageView.as_view(), name='manage'),
    path('routing/', views.routing, name='routing'),
    path('register', views.register_request, name='register'),
    path('manage/edit/', views.EditView.as_view(), name='edit'),
    path('add', views.add_request, name='add'),
    path('delete', views.del_request, name='delete'),
    path('toggle', views.toggle_request, name='toggle'),
]