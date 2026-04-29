from django.urls import path
from . import views

urlpatterns = [
    # Modül
    path('moduller/', views.modul_liste, name='modul_liste'),
    path('moduller/ekle/', views.modul_ekle, name='modul_ekle'),
    path('moduller/<int:pk>/guncelle/', views.modul_guncelle, name='modul_guncelle'),
    path('moduller/<int:pk>/sil/', views.modul_sil, name='modul_sil'),

    # Blog
    path('blog/', views.blog_liste, name='blog_liste'),
    path('blog/ekle/', views.blog_ekle, name='blog_ekle'),
    path('blog/<int:pk>/', views.blog_detay, name='blog_detay'),
    path('blog/<int:pk>/guncelle/', views.blog_guncelle, name='blog_guncelle'),
    path('blog/<int:pk>/sil/', views.blog_sil, name='blog_sil'),

    # Quiz
    path('quiz/', views.quiz_kategori, name='quiz_kategori'),
    path('quiz/<str:kategori>/', views.quiz_baslat, name='quiz_baslat'),
    path('quiz/sonuc/<int:pk>/', views.quiz_sonuc, name='quiz_sonuc'),

    # Leaderboard
    path('leaderboard/', views.leaderboard, name='leaderboard'),

    # Günlük
    path('gunluk/', views.gunluk_liste, name='gunluk_liste'),
    path('gunluk/ekle/', views.gunluk_ekle, name='gunluk_ekle'),
    path('gunluk/<int:pk>/guncelle/', views.gunluk_guncelle, name='gunluk_guncelle'),
    path('gunluk/<int:pk>/sil/', views.gunluk_sil, name='gunluk_sil'),

    # Kulüp & Forum
    path('forum/', views.kulup_liste, name='kulup_liste'),
    path('forum/kulup/olustur/', views.kulup_olustur, name='kulup_olustur'),
    path('forum/kulup/<int:pk>/', views.kulup_detay, name='kulup_detay'),
    path('forum/kulup/<int:pk>/katil/', views.kulup_katil, name='kulup_katil'),
    path('forum/kulup/<int:kulup_pk>/post/olustur/', views.post_olustur, name='post_olustur'),
    path('forum/post/<int:pk>/', views.post_detay, name='post_detay'),
    path('forum/post/<int:pk>/sil/', views.post_sil, name='post_sil'),
    path('forum/post/<int:pk>/begen/', views.post_begen, name='post_begen'),
    path('forum/yorum/<int:pk>/begen/', views.yorum_begen, name='yorum_begen'),
]