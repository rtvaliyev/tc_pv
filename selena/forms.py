from django import forms


class SelenaForm(forms.Form):
    number = forms.CharField(max_length=7,min_length=7, label=' Abunəçinin nömrəsi ')

class SelenaForm1(forms.Form):
    ipdslam = forms.CharField(max_length=100, label=' Dslam ')
    ipplata = forms.CharField(max_length=100, label=' Plata ')
    ipport = forms.CharField(max_length=100, label=' Port ')