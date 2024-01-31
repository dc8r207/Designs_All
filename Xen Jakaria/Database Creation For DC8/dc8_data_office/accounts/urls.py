
from django.urls import include, path
from drawing_cabinet import views as cabinetview
from .import views
urlpatterns = [   
    path("",cabinetview.index),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    
]