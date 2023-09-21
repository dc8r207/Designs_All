from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("vpc/", include("vip_canteen.urls")),
    path("admin/", admin.site.urls),
]