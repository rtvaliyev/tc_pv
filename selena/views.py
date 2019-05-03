from django.shortcuts import render, Http404, redirect
from django.http import HttpResponse
from .forms import SelenaForm
from .forms import SelenaForm1
from django.contrib import messages
from django.contrib.auth.models import User
import selenarequests as sr
import selenaunreg as su
import selenagone as sg
import selenasave as ss


def selena_view(request):
    if  not request.user.is_authenticated:
        return redirect('home')
    form = SelenaForm(request.POST or None)
    if form.is_valid():
        username = request.user.username
        u = User.objects.get(username__exact=username)
        password = u.password[8:]
        print ('  USER   : '+username)
        number = form.cleaned_data.get('number')
        a=sr.sellet(username,password,number)
        if a is None:
            return render(request, 'selena/err.html')
        if len(a)==6:
            context = {
                'aa':a[0][45:],
                'bb':a[1][45:],
                'cc':a[2][45:],
                'dd':a[3][45:],
                'ee':a[4][7:23],
                }
            return render(request, 'selena/detail64active.html',context)
        if len(a)==2:
            context = {
                'aa':a[0][25:44],
                'bb':a[0][68:],
                'cc':a[1][25:44],
                'dd':a[1][68:],
                }
            return render(request, 'selena/detailadslactive.html',context)
        if len(a)==3:
            context = {
                'aa':a[0][27:50],
                'bb':a[0][52:],
                'cc':a[1][27:50],
                'dd':a[1][52:],
                }
            return render(request, 'selena/detailvdslactive.html',context)
        if len(a)==5:
            context = {
                'aa':a[0][37:],
                'bb':a[1][37:],
                'cc':a[2][37:],
                'dd':a[3][37:],
                'ee':a[4][37:],
                }
            messages.success(request, 'Fiziki Qoşulmada "SNR" Göstəriciləri Düzgün Olmaya Bilər! Baxın:"Maksimum Sürət"')
            return render(request, 'selena/detail48active.html',context)
        else:
            context = {
                'aa':a[0],
                }
            return render(request, 'selena/detailnodsl.html',context)
    return render(request, 'selena/form.html', {'form':form})

def selena_view1(request): 
    form = SelenaForm1(request.POST or None)
    if form.is_valid():
        dslamip = form.cleaned_data.get('ipdslam')
        plataip = form.cleaned_data.get('ipplata')
        portip = form.cleaned_data.get('ipport')
        a=su.tellet(dslamip,plataip,portip)
        if a is None:
            return render(request, 'selena/err.html')
        if len(a)==6:
            context = {
                'aa':a[0][45:],
                'bb':a[1][45:],
                'cc':a[2][45:],
                'dd':a[3][45:],
                'ee':a[4][7:23],
                }
            return render(request, 'selena/detail64active.html',context)
        if len(a)==2:
            context = {
                'aa':a[0][25:44],
                'bb':a[0][68:],
                'cc':a[1][25:44],
                'dd':a[1][68:],
                }
            return render(request, 'selena/detailadslactive.html',context)
        if len(a)==3:
            context = {
                'aa':a[0][27:50],
                'bb':a[0][52:],
                'cc':a[1][27:50],
                'dd':a[1][52:],
                }
            return render(request, 'selena/detailvdslactive.html',context)
        if len(a)==5:
            context = {
                'aa':a[0][37:],
                'bb':a[1][37:],
                'cc':a[2][37:],
                'dd':a[3][37:],
                'ee':a[4][37:],
                }
            messages.success(request, 'Fiziki Qoşulmada "SNR" Göstəriciləri Düzgün Olmaya Bilər! Baxın:"Maksimum Sürət"')
            return render(request, 'selena/detail48active.html',context)
        else:
            context = {
                'aa':a[0],
                }
            return render(request, 'selena/detailnodsl.html',context)
    return render(request, 'selena/form.html', {'form':form})

def selena_view2(request):
    if  not request.user.is_authenticated:
        return redirect('home')
    groups = request.user.groups.all()
    if groups:
        role = groups[0].name
    if role == 'Texnik':
        form = SelenaForm(request.POST or None)
        if form.is_valid():
            print ('  GROUP  : '+role)
            username = request.user.username
            u = User.objects.get(username__exact=username)
            password = u.password[8:]
            print ('  USER   : '+username)
            number = form.cleaned_data.get('number')
            a=sg.gellet(username,password,number)
            if a is None:
                return render(request, 'selena/errspeed.html')
            if len(a)==5:
                context = {
                    'aa':a[0][:-1],
                    'bb':a[1],
                    'cc':a[2],
                    'dd':a[3],
                    'ee':a[4][2:],
                    }
                return render(request, 'selena/detail64activespeed.html',context)
        return render(request, 'selena/formspeed.html', {'form':form})
    else:
        return redirect('home')

def selena_save(request):
    if  not request.user.is_authenticated:
        return redirect('home')
    groups = request.user.groups.all()
    if groups:
        role = groups[0].name
    if role == 'Texnik':
        a=ss.savellet()
        print('  SAVED')
        if a is None:
            return render(request, 'selena/errspeed.html')
        else:
            f = open('resultselena.txt', 'r')
            content = f.read()
            context = {
                    'aa':content,
                    }
            f.close()
            return render(request, 'selena/resultselena.html',context)
    else:
        return redirect('home')

def selena_delete(request):
    if  not request.user.is_authenticated:
        return redirect('home')
    groups = request.user.groups.all()
    if groups:
        role = groups[0].name
    if role == 'Texnik':
        a=ss.delellet()
        return redirect('home')
    else:
        return redirect('home')

def view_404(request):
    return redirect('home')
