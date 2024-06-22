from django.urls import path, include
from .views.airlineView import AirlineView
from .views.airplaneView import AirplaneView
from .views.airportsView import AirportsView
from .views.routeView import RouteView
from django_request_mapping import UrlPattern

urlpattern = UrlPattern()
urlpattern.register(AirlineView)
urlpattern.register(AirplaneView)
urlpattern.register(AirportsView)
urlpattern.register(RouteView)

urlpatterns = [
    # path('', views.olympics),

    path('', include(urlpattern))
    #mirko gay
]
