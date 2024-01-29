from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse
from . import views

urlpatterns = [   
    #path("",views.index,name="drawing_list"),
    #path("upload_pdf/",views.upload_pdf,name='upload_pdf'),
    #path("upload_design/",views.upload_design,name='upload_design'),  
    #path(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    path("", views.book_list, name='book_list'),
    #path(r'^books/create/$', views.book_create, name='book_create'),
    #path(r'^books/(?P<pk>\d+)/update/$', views.book_update, name='book_update'),
    #path(r'^books/(?P<pk>\d+)/delete/$', views.book_delete, name='book_delete'),
    
]