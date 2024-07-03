from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('calling/', views.Call.as_view(), name='calling'),
]

