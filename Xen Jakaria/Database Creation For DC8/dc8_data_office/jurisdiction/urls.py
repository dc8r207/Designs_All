from django.urls import path
from .views import JurisdictionMapView

urlpatterns = [
   path("map/",JurisdictionMapView.as_view()), 
]
