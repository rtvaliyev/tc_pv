from django.shortcuts import render


def home_view(request):
    if request.user.is_authenticated:
        context = {
            'istfadi': request.user.username
        }
    else:
        context = {
            'istfadi': 'Salam,Qonaq!'
        }
    return render(request, 'home.html', context)