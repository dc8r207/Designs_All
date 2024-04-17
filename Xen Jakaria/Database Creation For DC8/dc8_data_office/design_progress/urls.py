from django.contrib import admin
from django.urls import include, path,re_path
from django.http import HttpResponse
from . import views

urlpatterns = [   
    path("",views.index,name="work_list"),
    path("create_design_work",views.create_design_work,name="create_design_work"),    
    re_path(r'^(?P<pk>\d+)/update/$', views.update_design_progress, name='update_design_progress'),
    re_path(r'^(?P<pk>\d+)/add_design_data/$', views.add_design_data, name='add_design_data'),
    re_path(r'^(?P<pk>\d+)/dowload_design_data/$', views.download_design_data, name='download_design_data'),
    #path("upload_pdf/",views.upload_pdf,name='upload_pdf'),
    #path("upload_design/",views.upload_design,name='upload_design'),
    #path("update_design/<int:id>/",views.update_design,name='update_design'),
    #path("delete_design/<int:pk>/",views.delete_design,name='delete_design'),
    #re_path(r'^design/(?P<pk>\d+)/update/$', views.update_design, name='update_design'),
    #re_path(r'^design/(?P<pk>\d+)/delete/$', views.delete_design, name='delete_design'),   
    
]