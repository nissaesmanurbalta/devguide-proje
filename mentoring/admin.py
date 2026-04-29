from django.contrib import admin
from .models import Appointment, Message, MentorTalebi, Patika, PatikaAdim


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'mentor', 'date', 'status']
    list_filter = ['status']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'created_at', 'is_read']


@admin.register(MentorTalebi)
class MentorTalebiAdmin(admin.ModelAdmin):
    list_display = ['ogrenci', 'mentor', 'status', 'created_at']
    list_filter = ['status']


@admin.register(Patika)
class PatikaAdmin(admin.ModelAdmin):
    list_display = ['baslik', 'mentor', 'seviye', 'created_at']
    list_filter = ['seviye']


@admin.register(PatikaAdim)
class PatikaAdimAdmin(admin.ModelAdmin):
    list_display = ['patika', 'sira', 'baslik']