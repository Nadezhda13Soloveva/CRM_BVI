from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('calling/', views.CallList.as_view(), name='calling'),
    path('updata/', views.updata, name='calling'),
]

