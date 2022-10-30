from django.shortcuts import redirect, render
from django.contrib import auth
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                _ = User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/register.html', {
                    'error' : 'Username has already been taken!'
                })
            except User.DoesNotExist:
                user = User.objects.create_user(
                    request.POST['username'],
                    password = request.POST['password1']
                )
                auth.login(request, user)
                return redirect('home')
        else:
            return render(request, 'accounts/register.html', {
                'error' : 'Passwords must match!'
            })
    else:
        return render(request, 'accounts/register.html')

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password1'])
        if user is not None:
            auth.login(request, user)
            if request.POST['next']!='':
                return redirect(request.POST['next'])
            else:
                return redirect('home')
        else:
            return render(request, 'accounts/login.html', {
                'error' : 'User not found! Username or Password is incorrect.'
            })
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')