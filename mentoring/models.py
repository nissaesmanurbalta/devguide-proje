from django.db import models
from django.contrib.auth.models import User


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('beklemede', 'Beklemede'),
        ('onaylandi', 'Onaylandı'),
        ('reddedildi', 'Reddedildi'),
    ]
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_appointments')
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentor_appointments')
    date = models.DateTimeField(verbose_name='Tarih')
    message = models.TextField(verbose_name='Mesaj', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='beklemede')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Randevu'
        verbose_name_plural = 'Randevular'

    def __str__(self):
        return f"{self.student.username} → {self.mentor.username}"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}"


class MentorTalebi(models.Model):
    STATUS_CHOICES = [
        ('beklemede', 'Beklemede'),
        ('onaylandi', 'Onaylandı'),
        ('reddedildi', 'Reddedildi'),
    ]
    ogrenci = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gonderilen_talepler')
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alinan_talepler')
    mesaj = models.TextField(blank=True, verbose_name='Tanışma Mesajı')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='beklemede')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['ogrenci', 'mentor']
        verbose_name = 'Mentor Talebi'
        verbose_name_plural = 'Mentor Talepleri'

    def __str__(self):
        return f"{self.ogrenci.username} → {self.mentor.username} ({self.status})"


class Patika(models.Model):
    SEVIYE_CHOICES = [
        ('baslangic', 'Başlangıç'),
        ('orta', 'Orta'),
        ('ileri', 'İleri'),
    ]
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patikaları')
    baslik = models.CharField(max_length=200, verbose_name='Patika Başlığı')
    aciklama = models.TextField(verbose_name='Açıklama')
    seviye = models.CharField(max_length=20, choices=SEVIYE_CHOICES, default='baslangic')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Patika'
        verbose_name_plural = 'Patikalar'

    def __str__(self):
        return f"{self.baslik} – {self.mentor.username}"


class PatikaAdim(models.Model):
    patika = models.ForeignKey(Patika, on_delete=models.CASCADE, related_name='adimlar')
    sira = models.PositiveIntegerField(default=1)
    baslik = models.CharField(max_length=200)
    aciklama = models.TextField()

    class Meta:
        ordering = ['sira']

    def __str__(self):
        return f"{self.patika.baslik} – Adım {self.sira}"