from django import forms
from .models import EducationModule, BlogPost, DevelopmentLog, Kulup, ForumPost, ForumYorum
class ModulForm(forms.ModelForm):
    class Meta:
        model = EducationModule
        fields = ['title', 'description', 'level', 'status']
        labels = {
            'title': 'Modül Başlığı',
            'description': 'Açıklama',
            'level': 'Seviye',
            'status': 'Durum',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Örn: Python Temelleri',
                'class': 'form-control-custom',
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Bu modülde ne öğreneceksin?',
                'class': 'form-control-custom',
            }),
            'level': forms.Select(attrs={'class': 'form-select-custom'}),
            'status': forms.Select(attrs={'class': 'form-select-custom'}),
        }
class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content']
        labels = {
            'title': 'Başlık',
            'content': 'İçerik',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Blog yazının başlığı...',
                'class': 'form-control-custom',
            }),
            'content': forms.Textarea(attrs={
                'rows': 10,
                'placeholder': 'Bugün ne öğrendin? Paylaş...',
                'class': 'form-control-custom',
            }),
        }

class GunlukForm(forms.ModelForm):
    class Meta:
        model = DevelopmentLog
        fields = ['title', 'content']
        labels = {
            'title': 'Başlık',
            'content': 'Bugün ne öğrendin?',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Örn: Django ForeignKey öğrendim',
                'class': 'form-control-custom',
            }),
            'content': forms.Textarea(attrs={
                'rows': 8,
                'placeholder': 'Bugün ne öğrendin, ne geliştirdin? Detaylıca yaz...',
                'class': 'form-control-custom',
            }),
        }
class KulupForm(forms.ModelForm):
    class Meta:
        model = Kulup
        fields = ['ad', 'aciklama']
        labels = {
            'ad': 'Kulüp Adı',
            'aciklama': 'Açıklama',
        }
        widgets = {
            'ad': forms.TextInput(attrs={
                'placeholder': 'Örn: Python Geliştiricileri',
                'class': 'form-control-custom',
            }),
            'aciklama': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Kulüp hakkında kısa bir açıklama...',
                'class': 'form-control-custom',
            }),
        }


class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['baslik', 'icerik']
        labels = {
            'baslik': 'Başlık',
            'icerik': 'İçerik',
        }
        widgets = {
            'baslik': forms.TextInput(attrs={
                'placeholder': 'Sorun veya konun nedir?',
                'class': 'form-control-custom',
            }),
            'icerik': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': 'Detaylı açıkla...',
                'class': 'form-control-custom',
            }),
        }


class ForumYorumForm(forms.ModelForm):
    class Meta:
        model = ForumYorum
        fields = ['icerik']
        labels = {'icerik': ''}
        widgets = {
            'icerik': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Cevabını veya yorumunu yaz...',
                'class': 'form-control-custom',
            }),
        }