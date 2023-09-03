from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm, LoginForm, UserEditForm
from .models import User
from .models import UserRole


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('main_page')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('main_page')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def main_page(request):
    if request.user.role == UserRole.MANAGER:
        users = User.objects.all()
    else:
        users = [request.user]

    return render(request, 'main.html', {'users': users})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You've been successfully logged out!")
    return redirect('login')


@login_required
def edit_user(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            updated_user = form.save(commit=False)
            if updated_user.role == UserRole.MANAGER:
                updated_user.is_staff = True
                updated_user.is_superuser = True
            else:
                updated_user.is_staff = False
                updated_user.is_superuser = False
            updated_user.save()
            return redirect('main_page')
    else:
        form = UserEditForm(instance=user)
    return render(request, 'edit_user.html', {'form': form})
