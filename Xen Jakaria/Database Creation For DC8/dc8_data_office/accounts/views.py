from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from .forms import UserCreationForm,LoginForm
from django.contrib.auth.forms import PasswordChangeForm
#signup page
def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})
# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                #return redirect('drawing_list')
                return redirect('work_list')
                
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})
#accounts/templates/accounts
# logout page
def user_logout(request):
    logout(request)
    return redirect('login')
from django.contrib.auth.views import PasswordChangeView  
from django.urls import reverse_lazy  
from .forms import PasswordChangingForm     
class PasswordsChangeView(PasswordChangeView): 
    form_class=PasswordChangingForm   
    #success_url=reverse_lazy('login')
    success_url=reverse_lazy('password_success')
    pass   
def password_success(request):
    return render (request,'accounts/passwordchange_success.html',{})
    pass        
        