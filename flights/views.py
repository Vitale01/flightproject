from django.shortcuts import render

# Create your Views here.
# flights/Views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
from .models import Route


def index(request):
    return render(request, 'index.html')

def servizi(request):
    return render(request, 'Servizi.html')
