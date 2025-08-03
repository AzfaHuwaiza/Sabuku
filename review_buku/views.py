from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import *
from .forms import *

def my_page(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user
    reviews = Review.objects.filter(user=user).order_by('-tanggal_submit')

    if request.method == 'POST':
        # Jika form edit nama lengkap dikirim
        if 'update_profile' in request.POST:
            full_name = request.POST.get('full_name', '').strip()

            if full_name:
                parts = full_name.split(None, 1)
                user.first_name = parts[0]
                user.last_name = parts[1] if len(parts) > 1 else ''
                user.save()
                messages.success(request, "Nama berhasil diperbarui.")
                return redirect('my_page')

        # Jika form edit review dikirim
        elif 'update_review' in request.POST:
            review_id = request.POST.get('review_id')
            judul_buku = request.POST.get('judul_buku')
            review_text = request.POST.get('review')

            review_obj = get_object_or_404(Review, id=review_id, user=user)
            review_obj.judul_buku = judul_buku
            review_obj.review = review_text

            if 'cover_buku' in request.FILES:
                review_obj.cover_buku = request.FILES['cover_buku']

            review_obj.save()
            messages.success(request, "Review berhasil diperbarui.")
            return redirect('my_page')

    return render(request, 'my_page.html', {'user': user, 'reviews': reviews})

def home(request):
    return render(request, 'home.html')

@login_required
def submit_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('my_page')
    else:
        form = ReviewForm()
    
    return render(request, 'submit_review.html', {'form': form})

def galeri_review(request):
    reviews = Review.objects.filter(status_approve=True).order_by('-tanggal_submit')
    return render(request, 'galeri_review.html', {'reviews': reviews})

@require_POST
@login_required
def edit_review(request):
    review_id = request.POST.get('review_id')
    review = get_object_or_404(Review, id=review_id, user=request.user)

    review.judul_buku = request.POST.get('judul_buku')
    review.penulis_buku = request.POST.get('penulis_buku')
    review.bulan_baca = request.POST.get('bulan_baca')
    review.isi_review = request.POST.get('isi_review')
    review.link_video = request.POST.get('link_video')

    # Ganti cover buku
    if request.FILES.get('cover_buku'):
        if review.cover_buku and review.cover_buku.path:
            review.cover_buku.delete(save=False)
        review.cover_buku = request.FILES['cover_buku']

    # Ganti infografis
    if request.FILES.get('gambar_infografis'):
        if review.gambar_infografis and review.gambar_infografis.path:
            review.gambar_infografis.delete(save=False)
        review.gambar_infografis = request.FILES['gambar_infografis']

    review.save()
    messages.success(request, "Review berhasil diperbarui.")
    return redirect('my_page')

@require_POST
@login_required
def delete_review(request):
    review_id = request.POST.get('review_id')
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if review.cover_buku and review.cover_buku.path:
        review.cover_buku.delete(save=False)
    if review.gambar_infografis and review.gambar_infografis.path:
        review.gambar_infografis.delete(save=False)

    review.delete()
    messages.success(request, "Review berhasil dihapus.")
    return redirect('my_page')

@login_required
def isi_nama(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        parts = full_name.split(None, 1)
        request.user.first_name = parts[0]
        request.user.last_name = parts[1] if len(parts) > 1 else ''
        request.user.save()
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    return redirect('home')
