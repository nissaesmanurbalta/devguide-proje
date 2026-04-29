from django.contrib import admin
from .models import EducationModule, BlogPost, QuizQuestion, QuizResult, DevelopmentLog, Kulup, ForumPost, ForumYorum


@admin.register(EducationModule)
class EducationModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'level', 'status', 'created_at']
    list_filter = ['level', 'status']
    search_fields = ['title', 'user__username']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at']
    search_fields = ['title', 'author__username']


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['soru', 'kategori', 'dogru_cevap', 'created_at']
    list_filter = ['kategori', 'dogru_cevap']
    search_fields = ['soru']


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'score', 'toplam_soru', 'kategori', 'created_at']
    list_filter = ['kategori']
    search_fields = ['user__username']


@admin.register(DevelopmentLog)
class DevelopmentLogAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at']
    search_fields = ['title', 'user__username']


@admin.register(Kulup)
class KulupAdmin(admin.ModelAdmin):
    list_display = ['ad', 'olusturan', 'uye_sayisi', 'created_at']
    search_fields = ['ad']


@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ['baslik', 'yazar', 'kulup', 'created_at']
    search_fields = ['baslik', 'yazar__username']


@admin.register(ForumYorum)
class ForumYorumAdmin(admin.ModelAdmin):
    list_display = ['yazar', 'post', 'created_at']
    search_fields = ['yazar__username']