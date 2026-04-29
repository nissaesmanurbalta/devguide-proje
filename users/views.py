from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import KayitFormu, ProfilFormu
from .models import Profile
from education.models import EducationModule
import requests as http_requests


def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'users/landing.html')


def kayit(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = KayitFormu(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(
                user=user,
                role=form.cleaned_data['role']
            )
            login(request, user)
            messages.success(request, 'Hoş geldin! Hesabın başarıyla oluşturuldu.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Lütfen formu doğru doldur.')
    else:
        form = KayitFormu()
    return render(request, 'users/kayit.html', {'form': form})


def giris(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Tekrar hoş geldin, {user.first_name}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Kullanıcı adı veya şifre hatalı.')
    return render(request, 'users/giris.html')


def cikis(request):
    logout(request)
    messages.info(request, 'Başarıyla çıkış yaptın.')
    return redirect('landing')


@login_required
def dashboard(request):
    profile = Profile.objects.get(user=request.user)
    modul_sayisi = EducationModule.objects.filter(user=request.user).count()

    # GitHub özet verisi
    github_data = None
    if profile.github_username:
        try:
            url = f'https://api.github.com/users/{profile.github_username}'
            response = http_requests.get(url, timeout=5)
            if response.status_code == 200:
                github_data = response.json()
        except Exception:
            pass

    # Motivasyon sözü API
    motivasyon = None
    try:
        r = http_requests.get('https://zenquotes.io/api/random', timeout=5)
        if r.status_code == 200:
            data = r.json()
            motivasyon = {
                'soz': data[0]['q'],
                'yazar': data[0]['a'],
            }
    except Exception:
        motivasyon = {
            'soz': 'Kod yazmak bir dil öğrenmek gibidir. Her gün pratik yaparsanız, bir gün akıcı konuşursunuz.',
            'yazar': 'DevGuide',
        }

    # Teknoloji haberleri (HackerNews API)
    haberler = []
    try:
        r = http_requests.get(
            'https://hacker-news.firebaseio.com/v0/topstories.json',
            timeout=5
        )
        if r.status_code == 200:
            haber_idler = r.json()[:5]
            for hid in haber_idler:
                try:
                    hr = http_requests.get(
                        f'https://hacker-news.firebaseio.com/v0/item/{hid}.json',
                        timeout=3
                    )
                    if hr.status_code == 200:
                        haber = hr.json()
                        if haber and haber.get('title') and haber.get('url'):
                            haberler.append({
                                'baslik': haber['title'],
                                'url': haber['url'],
                                'puan': haber.get('score', 0),
                            })
                except Exception:
                    continue
    except Exception:
        pass

    return render(request, 'users/dashboard.html', {
        'profile': profile,
        'modul_sayisi': modul_sayisi,
        'github_data': github_data,
        'motivasyon': motivasyon,
        'haberler': haberler,
    })


@login_required
def profil(request):
    profile = Profile.objects.get(user=request.user)


    mentor_bilgisi = None
    if profile.role == 'student':
        from mentoring.models import MentorTalebi
        onay = MentorTalebi.objects.filter(
            ogrenci=request.user, status='onaylandi'
        ).select_related('mentor').first()
        if onay:
            mentor_bilgisi = onay.mentor

    if request.method == 'POST':
        form = ProfilFormu(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil güncellendi.')
            return redirect('profil')
    else:
        form = ProfilFormu(instance=profile)

    return render(request, 'users/profil.html', {
        'form': form,
        'profile': profile,
        'mentor_bilgisi': mentor_bilgisi,
    })


@login_required
def github_profil(request):
    profile = Profile.objects.get(user=request.user)
    github_data = None
    hata = None

    if profile.github_username:
        try:
            url = f'https://api.github.com/users/{profile.github_username}'
            response = http_requests.get(url, timeout=5)
            if response.status_code == 200:
                github_data = response.json()
            elif response.status_code == 404:
                hata = 'GitHub kullanıcısı bulunamadı. Profil ayarlarından kullanıcı adını kontrol et.'
            else:
                hata = 'GitHub verisi alınamadı. Lütfen daha sonra tekrar dene.'
        except Exception:
            hata = 'Bağlantı hatası. İnternet bağlantını kontrol et.'
    else:
        hata = 'Henüz GitHub kullanıcı adı eklenmemiş. Profilinden ekleyebilirsin.'

    return render(request, 'users/github_profil.html', {
        'profile': profile,
        'github_data': github_data,
        'hata': hata,
    })