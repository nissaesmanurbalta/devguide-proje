from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('kayit/', views.kayit, name='kayit'),
    path('giris/', views.giris, name='giris'),
    path('cikis/', views.cikis, name='cikis'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profil/', views.profil, name='profil'),
    path('github/', views.github_profil, name='github_profil'),
]