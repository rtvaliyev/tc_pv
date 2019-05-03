from .views import selena_view, selena_view1, selena_view2, selena_save, selena_delete
from django.conf.urls import url

app_name = 'selena'

urlpatterns = [
    url(r'^selenareg/$', selena_view, name='selenareg'),
    url(r'^selenaunreg/$', selena_view1, name='selenaunreg'),
    url(r'^selenagone/$', selena_view2, name='selenagone'),
    url(r'^selenasave/$', selena_save, name='selenasave'),
    url(r'^selenadelete/$', selena_delete, name='selenadelete'),
]