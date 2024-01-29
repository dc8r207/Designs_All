from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse
from . import views

urlpatterns = [   
    path("",views.index,name="drawing_list"),
    path("upload_pdf/",views.upload_pdf,name='upload_pdf'),
    path("upload_design/",views.upload_design,name='upload_design'),  
    
]