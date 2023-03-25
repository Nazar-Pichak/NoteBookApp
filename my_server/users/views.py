from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import LoginForm, RegisterForm

def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})
    
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have signed up successfully')
            login(request, user)
            return redirect('posts')
        else:
            return render(request, 'users/register.html', {'form': form})
        

def sign_in(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            redirect('posts')

        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user:
                login(request, user)
                messages.success(request, f'Hi {username.title()} welcome back!')
                return redirect('posts')
            else:
                messages.error(request, 'Invalid password or username')
                return render(request, 'users/login.html', {'form': form})
            
def sign_out(request):
    logout(request)
    messages.success(request, 'You have logged out successfully')
    return redirect('posts')