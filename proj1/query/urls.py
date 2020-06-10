from django.urls import path
from . import views

urlpatterns = [
    path('', views.userQuery, name='user-query'),
    path('vidQuery/', views.vidQuery, name='vid-query'),
    path('response/', views.response, name='response'),
    path('queryCounts/', views.queryCounts, name='query-counts'),
    path('reset/', views.reset, name='reset')
]
