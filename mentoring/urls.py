from django.urls import path
from . import views

urlpatterns = [

    path('mentorler/', views.mentor_liste, name='mentor_liste'),
    path('mentorler/<int:mentor_id>/talep/', views.mentor_talep, name='mentor_talep'),
    path('talepler/', views.talep_yonet, name='talep_yonet'),
    path('talepler/<int:pk>/guncelle/', views.talep_guncelle, name='talep_guncelle'),

    path('mentorler/<int:mentor_id>/randevu/', views.randevu_olustur, name='randevu_olustur'),
    path('randevular/', views.randevu_liste, name='randevu_liste'),
    path('randevular/<int:pk>/guncelle/', views.randevu_guncelle, name='randevu_guncelle'),

    path('takvim/', views.takvim, name='takvim'),

    path('sohbet/', views.sohbet_liste, name='sohbet_liste'),
    path('sohbet/<int:kullanici_id>/', views.sohbet_detay, name='sohbet_detay'),

    path('ogrencilerim/', views.ogrenci_listesi, name='ogrenci_listesi'),
    path('ogrencilerim/<int:ogrenci_id>/', views.ogrenci_detay, name='ogrenci_detay'),

    path('patikalar/', views.patika_liste, name='patika_liste'),
    path('patikalar/olustur/', views.patika_olustur, name='patika_olustur'),
    path('patikalar/<int:pk>/', views.patika_detay, name='patika_detay'),
    path('patikalar/<int:patika_pk>/adim/', views.patika_adim_ekle, name='patika_adim_ekle'),
]