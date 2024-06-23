from django.urls import path, include
from django_request_mapping import UrlPattern
from .views.airlineView import AirlineView
from .views.airplaneView import AirplaneView
from .views.routeView import RouteView
from .views.airportsView import AirportView

urlpattern = UrlPattern()
urlpattern.register(AirlineView)
urlpattern.register(AirplaneView)
urlpattern.register(AirportView)
urlpattern.register(RouteView)

urlpatterns = [
    path('', include(urlpattern))
]
