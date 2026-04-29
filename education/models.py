from django.db import models
from django.contrib.auth.models import User


class EducationModule(models.Model):
    LEVEL_CHOICES = [
        ('baslangic', 'Başlangıç'),
        ('orta', 'Orta'),
        ('ileri', 'İleri'),
    ]
    STATUS_CHOICES = [
        ('devam', 'Devam Ediyor'),
        ('tamamlandi', 'Tamamlandı'),
        ('beklemede', 'Beklemede'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name='Başlık')
    description = models.TextField(verbose_name='Açıklama')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='baslangic', verbose_name='Seviye')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='beklemede', verbose_name='Durum')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Eğitim Modülü'
        verbose_name_plural = 'Eğitim Modülleri'

    def __str__(self):
        return f"{self.title} – {self.user.username}"
class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Yazar')
    title = models.CharField(max_length=200, verbose_name='Başlık')
    content = models.TextField(verbose_name='İçerik')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blog Yazısı'
        verbose_name_plural = 'Blog Yazıları'

    def __str__(self):
        return f"{self.title} – {self.author.username}"
class QuizQuestion(models.Model):
    KATEGORI_CHOICES = [
        ('python', 'Python'),
        ('django', 'Django'),
        ('genel', 'Genel Programlama'),
        ('veritabani', 'Veritabanı'),
        ('web', 'Web Geliştirme'),
    ]

    soru = models.TextField(verbose_name='Soru')
    secenek_a = models.CharField(max_length=200, verbose_name='Seçenek A')
    secenek_b = models.CharField(max_length=200, verbose_name='Seçenek B')
    secenek_c = models.CharField(max_length=200, verbose_name='Seçenek C')
    secenek_d = models.CharField(max_length=200, verbose_name='Seçenek D')
    dogru_cevap = models.CharField(
        max_length=1,
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')],
        verbose_name='Doğru Cevap'
    )
    kategori = models.CharField(max_length=20, choices=KATEGORI_CHOICES, default='genel')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Quiz Sorusu'
        verbose_name_plural = 'Quiz Soruları'

    def __str__(self):
        return f"{self.soru[:60]}..."


class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Kullanıcı')
    score = models.IntegerField(default=0, verbose_name='Skor')
    toplam_soru = models.IntegerField(default=0, verbose_name='Toplam Soru')
    kategori = models.CharField(max_length=20, default='genel')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score', '-created_at']
        verbose_name = 'Quiz Sonucu'
        verbose_name_plural = 'Quiz Sonuçları'

    def __str__(self):
        return f"{self.user.username} – {self.score} puan"

    def yuzde(self):
        if self.toplam_soru == 0:
            return 0
        return int((self.score / self.toplam_soru) * 100)

class DevelopmentLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Kullanıcı')
    title = models.CharField(max_length=200, verbose_name='Başlık')
    content = models.TextField(verbose_name='İçerik')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Gelişim Günlüğü'
        verbose_name_plural = 'Gelişim Günlükleri'

    def __str__(self):
        return f"{self.user.username} – {self.title}"
class Kulup(models.Model):
    ad = models.CharField(max_length=100, verbose_name='Kulüp Adı')
    aciklama = models.TextField(verbose_name='Açıklama')
    olusturan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='olusturulan_kulupler')
    uyeler = models.ManyToManyField(User, related_name='katildigi_kulupler', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Kulüp'
        verbose_name_plural = 'Kulüpler'

    def __str__(self):
        return self.ad

    def uye_sayisi(self):
        return self.uyeler.count()


class ForumPost(models.Model):
    kulup = models.ForeignKey(Kulup, on_delete=models.CASCADE, related_name='postlar')
    yazar = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_postlari')
    baslik = models.CharField(max_length=200, verbose_name='Başlık')
    icerik = models.TextField(verbose_name='İçerik')
    begeniler = models.ManyToManyField(User, related_name='begenilen_postlar', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Forum Gönderisi'
        verbose_name_plural = 'Forum Gönderileri'

    def __str__(self):
        return self.baslik

    def begeni_sayisi(self):
        return self.begeniler.count()

    def yorum_sayisi(self):
        return self.yorumlar.count()


class ForumYorum(models.Model):
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='yorumlar')
    yazar = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_yorumlari')
    icerik = models.TextField(verbose_name='Yorum')
    begeniler = models.ManyToManyField(User, related_name='begenilen_yorumlar', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Forum Yorumu'
        verbose_name_plural = 'Forum Yorumları'

    def __str__(self):
        return f"{self.yazar.username} – {self.post.baslik[:40]}"

    def begeni_sayisi(self):
        return self.begeniler.count()