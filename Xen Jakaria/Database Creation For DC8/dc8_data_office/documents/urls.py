from django.contrib import admin
from django.urls import include, path,re_path
from django.http import HttpResponse
from . import views

urlpatterns = [   
    #path("",views.index,name="drawing_list"),
    #path("upload_pdf/",views.upload_pdf,name='upload_pdf'),
    #path("upload_design/",views.upload_design,name='upload_design'),  
    #path(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    path("", views.document_list, name='document_list'),
    re_path(r'create/', views.document_create, name='document_create'),
    re_path(r'^(?P<pk>\d+)/update/$', views.document_update, name='document_update'),
    re_path(r'^(?P<pk>\d+)/delete/$', views.document_delete, name='document_delete'),
    #path(r'^books/(?P<pk>\d+)/update/$', views.book_update, name='book_update'),
    #path(r'^books/(?P<pk>\d+)/delete/$', views.book_delete, name='book_delete'),
    
]