from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse_lazy


def user_login(request):
    if request.user.is_authenticated:
        return redirect('post_list')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                next_url = request.GET.get('next', 'post_list')
                return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})


def user_register(request):
    if request.user.is_authenticated:
        return redirect('post_list')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now login.')
            return redirect('welcome')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})


def welcome_view(request):
    return render(request, 'registration/welcome.html')


def user_logout(request):
    username = request.user.username
    logout(request)
    messages.info(request, f'You have been logged out successfully, {username}!')
    return redirect('post_list')


@login_required
def user_profile(request):
    user_posts = request.user.blogpost_set.all().order_by('-created_at')
    user_comments = request.user.comment_set.all().order_by('-created_at')
    
    context = {
        'user_posts': user_posts,
        'user_comments': user_comments,
        'total_posts': user_posts.count(),
        'total_comments': user_comments.count(),
    }
    return render(request, 'registration/profile.html', context)
