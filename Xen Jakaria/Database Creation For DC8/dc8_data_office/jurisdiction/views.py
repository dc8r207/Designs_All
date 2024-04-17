from django.shortcuts import render
from django.views.generic.base import (TemplateView,)

class JurisdictionMapView(TemplateView):
    template_name="map.html"
    

# Create your views here.
