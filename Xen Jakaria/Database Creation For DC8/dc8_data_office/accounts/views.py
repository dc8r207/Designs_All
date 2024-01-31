from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from .forms import UserCreationForm,LoginForm

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
                return redirect('drawing_list')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})
#accounts/templates/accounts
# logout page
def user_logout(request):
    logout(request)
    return redirect('login')
            
            
             
        