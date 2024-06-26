from django.urls import path, include
from django_request_mapping import UrlPattern
from .Views.airlineView import AirlineView
from .Views.airplaneView import AirplaneView
from .Views.routeView import RouteView
from .Views.airportsView import AirportView
from . import views

urlpattern = UrlPattern()
urlpattern.register(AirlineView)
urlpattern.register(AirplaneView)
urlpattern.register(AirportView)
urlpattern.register(RouteView)

urlpatterns = [
    path('', views.index, name='index'),
    path('', include(urlpattern))
]
