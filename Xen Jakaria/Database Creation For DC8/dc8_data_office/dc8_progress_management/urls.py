from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse


urlpatterns = [
    #path("vpc/", include("vip_canteen.urls")),
    path("admin/", admin.site.urls),
    path("",include("accounts.urls")),
    
    
]