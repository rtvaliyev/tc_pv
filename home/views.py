from django.shortcuts import render
from django.contrib import messages


def home_view(request):
    client_address = request.META.get('REMOTE_ADDR')
    print ('  Site checked by : '+client_address)
    if request.user.is_authenticated:
        context = {
            'isim': request.user.username
        }
        messages.success(request, 'EDGE-CORE VƏ RAİSECOM SWITCH-LƏRİ QEYDİYYATLI USERLƏR YOXLAYA BİLƏRLƏR.')
    else:
        context = {
            'isim': ''
        }
        messages.success(request, 'EDGE-CORE VƏ RAİSECOM SWITCH-LƏRİ QEYDİYYATLI USERLƏR YOXLAYA BİLƏRLƏR.')
    return render(request, 'home.html', context)