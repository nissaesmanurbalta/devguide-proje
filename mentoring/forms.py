from django import forms
from .models import Appointment, Message, MentorTalebi, Patika, PatikaAdim


class RandevuForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'message']
        labels = {'date': 'Tarih ve Saat', 'message': 'Mesajın (isteğe bağlı)'}
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control-custom'}),
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Mentora iletmek istediğin bir şey var mı?', 'class': 'form-control-custom'}),
        }


class MesajForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        labels = {'content': ''}
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Mesajını yaz...', 'class': 'form-control-custom'}),
        }


class MentorTalebiForm(forms.ModelForm):
    class Meta:
        model = MentorTalebi
        fields = ['mesaj']
        labels = {'mesaj': 'Tanışma Mesajı (isteğe bağlı)'}
        widgets = {
            'mesaj': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Kendini tanıt, neden bu mentoru seçtiğini anlat...',
                'class': 'form-control-custom',
            }),
        }


class PatikaForm(forms.ModelForm):
    class Meta:
        model = Patika
        fields = ['baslik', 'aciklama', 'seviye']
        labels = {'baslik': 'Patika Başlığı', 'aciklama': 'Açıklama', 'seviye': 'Seviye'}
        widgets = {
            'baslik': forms.TextInput(attrs={'placeholder': 'Örn: Python\'a Giriş Patikası', 'class': 'form-control-custom'}),
            'aciklama': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Bu patika ne öğretir?', 'class': 'form-control-custom'}),
            'seviye': forms.Select(attrs={'class': 'form-select-custom'}),
        }


class PatikaAdimForm(forms.ModelForm):
    class Meta:
        model = PatikaAdim
        fields = ['sira', 'baslik', 'aciklama']
        labels = {'sira': 'Sıra No', 'baslik': 'Adım Başlığı', 'aciklama': 'Açıklama'}
        widgets = {
            'sira': forms.NumberInput(attrs={'class': 'form-control-custom', 'min': 1}),
            'baslik': forms.TextInput(attrs={'placeholder': 'Örn: Değişkenler ve Veri Tipleri', 'class': 'form-control-custom'}),
            'aciklama': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Bu adımda ne yapılacak?', 'class': 'form-control-custom'}),
        }