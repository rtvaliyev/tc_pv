from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label='İstifadəçi adı')
    password = forms.CharField(max_length=100, label='Şifrə', widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("İstifadəçi adı və ya Şifrə səhvdir!")
        return super(LoginForm, self).clean()

class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=100, label='İstifadəçi adı')
    password1 = forms.CharField(max_length=100, label='Şifrə', widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=100, label='Təkrar şifrə', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'password1',
            'password2',
        ]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Şifrələr eyni deyil!")
        return password2
