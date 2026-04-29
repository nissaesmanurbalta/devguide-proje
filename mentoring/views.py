from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from users.models import Profile
from education.models import EducationModule, DevelopmentLog
from .models import Appointment, Message, MentorTalebi, Patika, PatikaAdim
from .forms import RandevuForm, MesajForm, MentorTalebiForm, PatikaForm, PatikaAdimForm



@login_required
def mentor_liste(request):
    mentorler = Profile.objects.filter(role='mentor').select_related('user')
    profil = Profile.objects.get(user=request.user)

    # Öğrencinin gönderdiği talepler
    talepler = {}
    if profil.role == 'student':
        for t in MentorTalebi.objects.filter(ogrenci=request.user):
            talepler[t.mentor_id] = t.status

    return render(request, 'mentoring/mentor_liste.html', {
        'mentorler': mentorler,
        'profil': profil,
        'talepler': talepler,
    })


@login_required
def mentor_talep(request, mentor_id):
    mentor = get_object_or_404(User, pk=mentor_id)
    mentor_profil = get_object_or_404(Profile, user=mentor, role='mentor')
    profil = get_object_or_404(Profile, user=request.user)

    if profil.role != 'student':
        messages.error(request, 'Sadece öğrenciler mentor talebi gönderebilir.')
        return redirect('mentor_liste')

    mevcut = MentorTalebi.objects.filter(ogrenci=request.user, mentor=mentor).first()
    if mevcut:
        messages.info(request, 'Bu mentora zaten talep göndermişsin.')
        return redirect('mentor_liste')

    if request.method == 'POST':
        form = MentorTalebiForm(request.POST)
        if form.is_valid():
            talep = form.save(commit=False)
            talep.ogrenci = request.user
            talep.mentor = mentor
            talep.save()
            messages.success(request, f'{mentor.get_full_name()} adlı mentora talep gönderildi!')
            return redirect('mentor_liste')
    else:
        form = MentorTalebiForm()

    return render(request, 'mentoring/mentor_talep_form.html', {
        'form': form,
        'mentor': mentor,
        'mentor_profil': mentor_profil,
    })


@login_required
def talep_yonet(request):
    profil = get_object_or_404(Profile, user=request.user)

    if profil.role == 'mentor':
        talepler = MentorTalebi.objects.filter(mentor=request.user).select_related('ogrenci')
    else:
        talepler = MentorTalebi.objects.filter(ogrenci=request.user).select_related('mentor')

    return render(request, 'mentoring/talep_liste.html', {
        'talepler': talepler,
        'profil': profil,
    })


@login_required
def talep_guncelle(request, pk):
    talep = get_object_or_404(MentorTalebi, pk=pk, mentor=request.user)
    if request.method == 'POST':
        yeni_status = request.POST.get('status')
        if yeni_status in ['onaylandi', 'reddedildi']:
            talep.status = yeni_status
            talep.save()
            if yeni_status == 'onaylandi':
                messages.success(request, f'{talep.ogrenci.get_full_name()} adlı öğrenci kabul edildi.')
            else:
                messages.info(request, 'Talep reddedildi.')
    return redirect('talep_yonet')


@login_required
def randevu_olustur(request, mentor_id):
    mentor = get_object_or_404(User, pk=mentor_id)
    profil = get_object_or_404(Profile, user=request.user)

    talep = MentorTalebi.objects.filter(
        ogrenci=request.user, mentor=mentor, status='onaylandi'
    ).first()

    if not talep:
        messages.error(request, 'Randevu almak için önce mentor talebinin onaylanması gerekiyor.')
        return redirect('mentor_liste')

    if request.method == 'POST':
        form = RandevuForm(request.POST)
        if form.is_valid():
            randevu = form.save(commit=False)
            randevu.student = request.user
            randevu.mentor = mentor
            randevu.save()
            messages.success(request, 'Randevu talebi oluşturuldu!')
            return redirect('randevu_liste')
    else:
        form = RandevuForm()

    return render(request, 'mentoring/randevu_form.html', {
        'form': form,
        'mentor': mentor,
    })


@login_required
def randevu_liste(request):
    profil = get_object_or_404(Profile, user=request.user)
    if profil.role == 'mentor':
        randevular = Appointment.objects.filter(mentor=request.user)
    else:
        randevular = Appointment.objects.filter(student=request.user)

    return render(request, 'mentoring/randevu_liste.html', {
        'randevular': randevular,
        'profil': profil,
    })


@login_required
def randevu_guncelle(request, pk):
    randevu = get_object_or_404(Appointment, pk=pk, mentor=request.user)
    if request.method == 'POST':
        yeni_status = request.POST.get('status')
        if yeni_status in ['onaylandi', 'reddedildi']:
            randevu.status = yeni_status
            randevu.save()
            messages.success(request, 'Randevu güncellendi.')
    return redirect('randevu_liste')


@login_required
def takvim(request):
    profil = get_object_or_404(Profile, user=request.user)
    if profil.role == 'mentor':
        randevular = Appointment.objects.filter(
            mentor=request.user, status='onaylandi'
        ).order_by('date')
    else:
        randevular = Appointment.objects.filter(
            student=request.user, status='onaylandi'
        ).order_by('date')

    return render(request, 'mentoring/takvim.html', {
        'randevular': randevular,
        'profil': profil,
    })


@login_required
def sohbet_liste(request):
    profil = get_object_or_404(Profile, user=request.user)

    if profil.role == 'mentor':

        onaylanan_ids = MentorTalebi.objects.filter(
            mentor=request.user, status='onaylandi'
        ).values_list('ogrenci_id', flat=True)
        kisiler = User.objects.filter(id__in=onaylanan_ids)
    else:

        onaylanan_ids = MentorTalebi.objects.filter(
            ogrenci=request.user, status='onaylandi'
        ).values_list('mentor_id', flat=True)
        kisiler = User.objects.filter(id__in=onaylanan_ids)

    return render(request, 'mentoring/sohbet_liste.html', {
        'kisiler': kisiler,
        'profil': profil,
    })


@login_required
def sohbet_detay(request, kullanici_id):
    diger = get_object_or_404(User, pk=kullanici_id)
    profil = get_object_or_404(Profile, user=request.user)


    if profil.role == 'student':
        izin = MentorTalebi.objects.filter(
            ogrenci=request.user, mentor=diger, status='onaylandi'
        ).exists()
    else:
        izin = MentorTalebi.objects.filter(
            ogrenci=diger, mentor=request.user, status='onaylandi'
        ).exists()

    if not izin:
        messages.error(request, 'Bu kullanıcıyla mesajlaşma izniniz yok.')
        return redirect('sohbet_liste')

    if request.method == 'POST':
        form = MesajForm(request.POST)
        if form.is_valid():
            mesaj = form.save(commit=False)
            mesaj.sender = request.user
            mesaj.receiver = diger
            mesaj.save()
            return redirect('sohbet_detay', kullanici_id=kullanici_id)
    else:
        form = MesajForm()

    mesajlar = Message.objects.filter(
        Q(sender=request.user, receiver=diger) |
        Q(sender=diger, receiver=request.user)
    ).order_by('created_at')

    mesajlar.filter(receiver=request.user, is_read=False).update(is_read=True)

    return render(request, 'mentoring/sohbet_detay.html', {
        'diger_kullanici': diger,
        'mesajlar': mesajlar,
        'form': form,
    })


@login_required
def ogrenci_listesi(request):
    profil = get_object_or_404(Profile, user=request.user)
    if profil.role != 'mentor':
        return redirect('dashboard')

    ogrenciler = MentorTalebi.objects.filter(
        mentor=request.user, status='onaylandi'
    ).select_related('ogrenci')

    return render(request, 'mentoring/ogrenci_listesi.html', {
        'ogrenciler': ogrenciler,
    })


@login_required
def ogrenci_detay(request, ogrenci_id):
    profil = get_object_or_404(Profile, user=request.user)
    if profil.role != 'mentor':
        return redirect('dashboard')


    talep = get_object_or_404(
        MentorTalebi, mentor=request.user,
        ogrenci_id=ogrenci_id, status='onaylandi'
    )

    ogrenci = talep.ogrenci
    ogrenci_profil = get_object_or_404(Profile, user=ogrenci)
    gunlukler = DevelopmentLog.objects.filter(user=ogrenci).order_by('-created_at')
    moduller = EducationModule.objects.filter(user=ogrenci)

    return render(request, 'mentoring/ogrenci_detay.html', {
        'ogrenci': ogrenci,
        'ogrenci_profil': ogrenci_profil,
        'gunlukler': gunlukler,
        'moduller': moduller,
    })


@login_required
def patika_liste(request):
    patikalar = Patika.objects.all().select_related('mentor')
    return render(request, 'mentoring/patika_liste.html', {'patikalar': patikalar})


@login_required
def patika_olustur(request):
    profil = get_object_or_404(Profile, user=request.user)
    if profil.role != 'mentor':
        messages.error(request, 'Sadece mentorlar patika oluşturabilir.')
        return redirect('patika_liste')

    if request.method == 'POST':
        form = PatikaForm(request.POST)
        if form.is_valid():
            patika = form.save(commit=False)
            patika.mentor = request.user
            patika.save()
            messages.success(request, f'"{patika.baslik}" patikası oluşturuldu!')
            return redirect('patika_detay', pk=patika.pk)
    else:
        form = PatikaForm()

    return render(request, 'mentoring/patika_form.html', {
        'form': form,
        'islem': 'Yeni Patika Oluştur',
        'buton': 'Oluştur',
    })


@login_required
def patika_detay(request, pk):
    patika = get_object_or_404(Patika, pk=pk)
    adimlar = patika.adimlar.all()
    profil = get_object_or_404(Profile, user=request.user)
    return render(request, 'mentoring/patika_detay.html', {
        'patika': patika,
        'adimlar': adimlar,
        'profil': profil,
    })


@login_required
def patika_adim_ekle(request, patika_pk):
    patika = get_object_or_404(Patika, pk=patika_pk, mentor=request.user)

    if request.method == 'POST':
        form = PatikaAdimForm(request.POST)
        if form.is_valid():
            adim = form.save(commit=False)
            adim.patika = patika
            adim.save()
            messages.success(request, 'Adım eklendi.')
            return redirect('patika_detay', pk=patika.pk)
    else:
        form = PatikaAdimForm()

    return render(request, 'mentoring/patika_adim_form.html', {
        'form': form,
        'patika': patika,
    })