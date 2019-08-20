from django.shortcuts import render, redirect, Http404
from .forms import  LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Group


def login_view(request):
    if request.user.is_authenticated:
        # raise Http404
        return redirect('home') 
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username,password=password)
        login(request,user)
        return redirect('home')
    return render(request, 'accounts/form.html',{'form':form, 'title': 'Giriş'})

def logout_view(request):
    if not request.user.is_authenticated:
        # raise Http404
        return redirect('home')
    logout(request)
    return redirect('home')

def register_view(request):
    if request.user.is_authenticated:
        # raise Http404
        return redirect('home')
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password1')
        user.set_password(password)
        # user.is_staff = user.is_superuser = True
        user.save()
        group = Group.objects.get(name='Operator')
        user.groups.add(group)
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect('home')
    messages.success(request, 'Qiqqət! Qeydiyyat zamanı "XXX BILLING"-in istifadəçi adı və şifrəsi saytın bazasında saxlanılır.')
    return render(request, "accounts/form.html", {"form": form, 'title': 'Qeydiyyat'})