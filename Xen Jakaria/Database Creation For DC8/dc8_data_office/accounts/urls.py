
from django.urls import include, path
from drawing_cabinet import views as cabinetview
from design_progress import views as progressView
from django.contrib.auth import views as auth_views
from .import views
urlpatterns = [   
    path("",progressView.index),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('password/',views.PasswordsChangeView.as_view(template_name="accounts/change_password.html"),name="password_change"),
    path('password_sucess/',views.password_success,name='password_success'),
]