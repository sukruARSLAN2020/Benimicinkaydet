from django import forms

class LoginForm(forms.form):
    username=forms.CharField(max_length=100,label='Kullancı Adı')
    password=forms.CharField(max_length=100,Label='Kullanıcı Şifresi',widget=PasswordInput)


