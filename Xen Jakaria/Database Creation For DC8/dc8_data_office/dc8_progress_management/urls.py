from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse
#serving user uploaded file during devlopment
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path("vpc/", include("vip_canteen.urls")),
    path("admin/", admin.site.urls),
    path("",include("accounts.urls")),
    path("drawing_cabinet/",include("drawing_cabinet.urls")),
     path("books/",include("books.urls")),
    
]
urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
