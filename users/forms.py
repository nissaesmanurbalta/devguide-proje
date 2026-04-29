from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class KayitFormu(UserCreationForm):
    email = forms.EmailField(required=True, label='E-posta')
    first_name = forms.CharField(max_length=50, required=True, label='Ad')
    last_name = forms.CharField(max_length=50, required=True, label='Soyad')
    role = forms.ChoiceField(
        choices=[('student', 'Öğrenci'), ('mentor', 'Mentor')],
        label='Rol'
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'username': 'Kullanıcı Adı',
        }

class ProfilFormu(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['github_username', 'bio']
        labels = {
            'github_username': 'GitHub Kullanıcı Adı',
            'bio': 'Hakkımda',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
