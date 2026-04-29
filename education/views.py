from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import Profile
from .models import EducationModule, BlogPost, QuizQuestion, QuizResult, DevelopmentLog, Kulup, ForumPost, ForumYorum
from .forms import ModulForm, BlogForm, GunlukForm, KulupForm, ForumPostForm, ForumYorumForm


@login_required
def modul_liste(request):
    moduller = EducationModule.objects.filter(user=request.user)

    # Filtreleme
    status_filtre = request.GET.get('status', '')
    level_filtre = request.GET.get('level', '')

    if status_filtre:
        moduller = moduller.filter(status=status_filtre)
    if level_filtre:
        moduller = moduller.filter(level=level_filtre)

    # İstatistikler
    tum_moduller = EducationModule.objects.filter(user=request.user)
    istatistik = {
        'toplam': tum_moduller.count(),
        'tamamlandi': tum_moduller.filter(status='tamamlandi').count(),
        'devam': tum_moduller.filter(status='devam').count(),
        'beklemede': tum_moduller.filter(status='beklemede').count(),
    }

    return render(request, 'education/modul_liste.html', {
        'moduller': moduller,
        'istatistik': istatistik,
        'status_filtre': status_filtre,
        'level_filtre': level_filtre,
    })


@login_required
def modul_ekle(request):
    if request.method == 'POST':
        form = ModulForm(request.POST)
        if form.is_valid():
            modul = form.save(commit=False)
            modul.user = request.user
            modul.save()
            messages.success(request, f'"{modul.title}" modülü başarıyla eklendi!')
            return redirect('modul_liste')
        else:
            messages.error(request, 'Lütfen formu eksiksiz doldur.')
    else:
        form = ModulForm()
    return render(request, 'education/modul_form.html', {
        'form': form,
        'islem': 'Yeni Modül Ekle',
        'buton': 'Ekle',
    })


@login_required
def modul_guncelle(request, pk):
    modul = get_object_or_404(EducationModule, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ModulForm(request.POST, instance=modul)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{modul.title}" modülü güncellendi.')
            return redirect('modul_liste')
        else:
            messages.error(request, 'Lütfen formu eksiksiz doldur.')
    else:
        form = ModulForm(instance=modul)
    return render(request, 'education/modul_form.html', {
        'form': form,
        'modul': modul,
        'islem': 'Modülü Düzenle',
        'buton': 'Güncelle',
    })


@login_required
def modul_sil(request, pk):
    modul = get_object_or_404(EducationModule, pk=pk, user=request.user)
    if request.method == 'POST':
        baslik = modul.title
        modul.delete()
        messages.success(request, f'"{baslik}" modülü silindi.')
        return redirect('modul_liste')
    return render(request, 'education/modul_sil.html', {'modul': modul})

def blog_liste(request):
    yazilar = BlogPost.objects.all()
    return render(request, 'education/blog_liste.html', {'yazilar': yazilar})


@login_required
def blog_ekle(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            yazi = form.save(commit=False)
            yazi.author = request.user
            yazi.save()
            messages.success(request, f'"{yazi.title}" başarıyla yayınlandı!')
            return redirect('blog_liste')
        else:
            messages.error(request, 'Lütfen formu eksiksiz doldur.')
    else:
        form = BlogForm()
    return render(request, 'education/blog_form.html', {
        'form': form,
        'islem': 'Yeni Blog Yazısı',
        'buton': 'Yayınla',
    })


def blog_detay(request, pk):
    yazi = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'education/blog_detay.html', {'yazi': yazi})


@login_required
def blog_guncelle(request, pk):
    yazi = get_object_or_404(BlogPost, pk=pk, author=request.user)
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=yazi)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{yazi.title}" güncellendi.')
            return redirect('blog_detay', pk=yazi.pk)
        else:
            messages.error(request, 'Lütfen formu eksiksiz doldur.')
    else:
        form = BlogForm(instance=yazi)
    return render(request, 'education/blog_form.html', {
        'form': form,
        'yazi': yazi,
        'islem': 'Blog Yazısını Düzenle',
        'buton': 'Güncelle',
    })


@login_required
def blog_sil(request, pk):
    yazi = get_object_or_404(BlogPost, pk=pk, author=request.user)
    if request.method == 'POST':
        baslik = yazi.title
        yazi.delete()
        messages.success(request, f'"{baslik}" silindi.')
        return redirect('blog_liste')
    return render(request, 'education/blog_sil.html', {'yazi': yazi})

@login_required
def quiz_kategori(request):
    kategoriler = QuizQuestion.KATEGORI_CHOICES
    en_iyi_skor = QuizResult.objects.filter(user=request.user).order_by('-score').first()
    return render(request, 'education/quiz_kategori.html', {
        'kategoriler': kategoriler,
        'en_iyi_skor': en_iyi_skor,
    })


@login_required
def quiz_baslat(request, kategori):
    gecerli_kategoriler = [k[0] for k in QuizQuestion.KATEGORI_CHOICES]
    if kategori not in gecerli_kategoriler:
        messages.error(request, 'Geçersiz kategori.')
        return redirect('quiz_kategori')

    sorular = list(QuizQuestion.objects.filter(kategori=kategori))

    if not sorular:
        messages.error(request, 'Bu kategoride henüz soru yok.')
        return redirect('quiz_kategori')

    if request.method == 'POST':
        skor = 0
        for soru in sorular:
            verilen_cevap = request.POST.get(f'soru_{soru.pk}', '')
            if verilen_cevap == soru.dogru_cevap:
                skor += 1

        sonuc = QuizResult.objects.create(
            user=request.user,
            score=skor,
            toplam_soru=len(sorular),
            kategori=kategori,
        )
        messages.success(request, f'Quiz tamamlandı! {len(sorular)} sorudan {skor} doğru.')
        return redirect('quiz_sonuc', pk=sonuc.pk)

    return render(request, 'education/quiz_baslat.html', {
        'sorular': sorular,
        'kategori': kategori,
        'kategori_adi': dict(QuizQuestion.KATEGORI_CHOICES).get(kategori, kategori),
    })


@login_required
def quiz_sonuc(request, pk):
    sonuc = get_object_or_404(QuizResult, pk=pk, user=request.user)
    return render(request, 'education/quiz_sonuc.html', {'sonuc': sonuc})


def leaderboard(request):
    from django.db.models import Max
    # Her kullanıcının en yüksek skoru
    skorlar = QuizResult.objects.values(
        'user__username', 'user__first_name', 'user__last_name', 'user__id'
    ).annotate(en_yuksek=Max('score')).order_by('-en_yuksek')[:20]

    return render(request, 'education/leaderboard.html', {'skorlar': skorlar})

@login_required
def gunluk_liste(request):
    profil = Profile.objects.get(user=request.user)

    if profil.role == 'mentor':
        gunlukler = DevelopmentLog.objects.all().select_related('user')
    else:
        gunlukler = DevelopmentLog.objects.filter(user=request.user)

    return render(request, 'education/gunluk_liste.html', {
        'gunlukler': gunlukler,
        'profil': profil,
    })


@login_required
def gunluk_ekle(request):
    profil = Profile.objects.get(user=request.user)
    if profil.role == 'mentor':
        messages.error(request, 'Mentorler günlük ekleyemez.')
        return redirect('gunluk_liste')

    if request.method == 'POST':
        form = GunlukForm(request.POST)
        if form.is_valid():
            gunluk = form.save(commit=False)
            gunluk.user = request.user
            gunluk.save()
            messages.success(request, f'"{gunluk.title}" günlüğe eklendi!')
            return redirect('gunluk_liste')
        else:
            messages.error(request, 'Lütfen formu eksiksiz doldur.')
    else:
        form = GunlukForm()

    return render(request, 'education/gunluk_form.html', {
        'form': form,
        'islem': 'Yeni Günlük Yaz',
        'buton': 'Kaydet',
    })


@login_required
def gunluk_guncelle(request, pk):
    gunluk = get_object_or_404(DevelopmentLog, pk=pk, user=request.user)

    if request.method == 'POST':
        form = GunlukForm(request.POST, instance=gunluk)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{gunluk.title}" güncellendi.')
            return redirect('gunluk_liste')
        else:
            messages.error(request, 'Lütfen formu eksiksiz doldur.')
    else:
        form = GunlukForm(instance=gunluk)

    return render(request, 'education/gunluk_form.html', {
        'form': form,
        'gunluk': gunluk,
        'islem': 'Günlüğü Düzenle',
        'buton': 'Güncelle',
    })


@login_required
def gunluk_sil(request, pk):
    gunluk = get_object_or_404(DevelopmentLog, pk=pk, user=request.user)

    if request.method == 'POST':
        baslik = gunluk.title
        gunluk.delete()
        messages.success(request, f'"{baslik}" silindi.')
        return redirect('gunluk_liste')

    return render(request, 'education/gunluk_sil.html', {'gunluk': gunluk})

@login_required
def kulup_liste(request):
    kulupler = Kulup.objects.all()
    katildiklari = request.user.katildigi_kulupler.all()
    return render(request, 'education/kulup_liste.html', {
        'kulupler': kulupler,
        'katildiklari': katildiklari,
    })


@login_required
def kulup_olustur(request):
    if request.method == 'POST':
        form = KulupForm(request.POST)
        if form.is_valid():
            kulup = form.save(commit=False)
            kulup.olusturan = request.user
            kulup.save()
            kulup.uyeler.add(request.user)
            messages.success(request, f'"{kulup.ad}" kulübü oluşturuldu!')
            return redirect('kulup_detay', pk=kulup.pk)
        else:
            messages.error(request, 'Lütfen formu eksiksiz doldur.')
    else:
        form = KulupForm()
    return render(request, 'education/kulup_form.html', {
        'form': form,
        'islem': 'Yeni Kulüp Oluştur',
        'buton': 'Oluştur',
    })


@login_required
def kulup_detay(request, pk):
    kulup = get_object_or_404(Kulup, pk=pk)
    postlar = ForumPost.objects.filter(kulup=kulup)
    uye_mi = request.user in kulup.uyeler.all()
    return render(request, 'education/kulup_detay.html', {
        'kulup': kulup,
        'postlar': postlar,
        'uye_mi': uye_mi,
    })


@login_required
def kulup_katil(request, pk):
    kulup = get_object_or_404(Kulup, pk=pk)
    if request.user in kulup.uyeler.all():
        kulup.uyeler.remove(request.user)
        messages.info(request, f'"{kulup.ad}" kulübünden ayrıldın.')
    else:
        kulup.uyeler.add(request.user)
        messages.success(request, f'"{kulup.ad}" kulübüne katıldın!')
    return redirect('kulup_detay', pk=pk)

@login_required
def post_olustur(request, kulup_pk):
    kulup = get_object_or_404(Kulup, pk=kulup_pk)

    if request.user not in kulup.uyeler.all():
        messages.error(request, 'Gönderi oluşturmak için önce kulübe katılmalısın.')
        return redirect('kulup_detay', pk=kulup_pk)

    if request.method == 'POST':
        form = ForumPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.kulup = kulup
            post.yazar = request.user
            post.save()
            messages.success(request, 'Gönderi oluşturuldu!')
            return redirect('post_detay', pk=post.pk)
        else:
            messages.error(request, 'Lütfen formu eksiksiz doldur.')
    else:
        form = ForumPostForm()

    return render(request, 'education/post_form.html', {
        'form': form,
        'kulup': kulup,
        'islem': 'Yeni Gönderi',
        'buton': 'Paylaş',
    })


@login_required
def post_detay(request, pk):
    post = get_object_or_404(ForumPost, pk=pk)
    yorumlar = ForumYorum.objects.filter(post=post)
    begendim = request.user in post.begeniler.all()

    if request.method == 'POST':
        form = ForumYorumForm(request.POST)
        if form.is_valid():
            yorum = form.save(commit=False)
            yorum.post = post
            yorum.yazar = request.user
            yorum.save()
            return redirect('post_detay', pk=pk)
        else:
            messages.error(request, 'Yorum boş olamaz.')
    else:
        form = ForumYorumForm()

    return render(request, 'education/post_detay.html', {
        'post': post,
        'yorumlar': yorumlar,
        'form': form,
        'begendim': begendim,
    })


@login_required
def post_sil(request, pk):
    post = get_object_or_404(ForumPost, pk=pk, yazar=request.user)
    kulup_pk = post.kulup.pk
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Gönderi silindi.')
        return redirect('kulup_detay', pk=kulup_pk)
    return render(request, 'education/post_sil.html', {'post': post})

@login_required
def post_begen(request, pk):
    post = get_object_or_404(ForumPost, pk=pk)
    if request.user in post.begeniler.all():
        post.begeniler.remove(request.user)
    else:
        post.begeniler.add(request.user)
    return redirect('post_detay', pk=pk)


@login_required
def yorum_begen(request, pk):
    yorum = get_object_or_404(ForumYorum, pk=pk)
    if request.user in yorum.begeniler.all():
        yorum.begeniler.remove(request.user)
    else:
        yorum.begeniler.add(request.user)
    return redirect('post_detay', pk=yorum.post.pk)