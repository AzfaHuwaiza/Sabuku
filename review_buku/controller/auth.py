from django.utils.http import urlsafe_base64_encode, url_has_allowed_host_and_scheme
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from review_buku.models import *
from review_buku.forms import *
import re

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            allowed_prefixes = ['227007', '237007', '247007', '257007', '267007', '277007', '287007']
            prefix = email.split('@')[0][:6]

            if not email.endswith('@student.unsil.ac.id'):
                messages.error(request, 'Email harus menggunakan akun Universitas Siliwangi')
                return render(request, 'register.html', {'form': form})

            if prefix not in allowed_prefixes:
                messages.error(request, 'Akun ini bukan mahasiswa Sistem Informasi UNSIL.')
                return render(request, 'register.html', {'form': form})

            user = form.save(commit=False)
            user.is_active = False  
            user.save()

            send_verification_email(request, user)
            messages.success(request, 'Akun berhasil dibuat. Silakan cek email untuk verifikasi.')

            return redirect('login')
        else:
            messages.error(request, 'Formulir tidak valid. Periksa kembali isianmu.')

    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

def verifikasi_terkirim_view(request):
    return render(request, 'verifikasi_terkirim.html')

def send_verification_email(request, user):
    current_site = get_current_site(request)
    subject = 'Aktivasi Akun'
    message = render_to_string('email_verifikasi.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

def activate_account(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login') 
    else:
        return HttpResponse('Link tidak valid atau sudah kedaluwarsa.')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        prefix = email.split('@')[0][:6]
        allowed_prefixes = ['227007', '237007', '247007', '257007', '267007', '277007', '287007']

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)

            next_url = request.GET.get('next')
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)

            return redirect('my_page')  
        else:
            messages.error(request, 'Email atau password salah.')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
