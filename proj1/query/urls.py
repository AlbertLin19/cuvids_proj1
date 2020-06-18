from django.urls import path
from . import views

urlpatterns = [
    path('', views.userQuery, name='user-query'),
    path('vidQuery/', views.vidQuery, name='vid-query'),
    path('response/', views.response, name='response'),
    path('queryCounts/', views.queryCounts, name='query-counts'),
    path('reset/', views.reset, name='reset'),
    path('newUserQuery/', views.newUserQuery, name='new-user-query'),
    path('newVidQuery/', views.newVidQuery, name='new-vid-query'),
    path('newUserResponse/', views.newUserResponse, name='new-user-response'),
    path('newVidResponse/', views.newVidResponse, name='new-vid-response')
]
