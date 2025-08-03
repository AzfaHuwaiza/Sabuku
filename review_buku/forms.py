from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'npm@student.unsil.ac.id',
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-blue transition'
        })
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-blue transition'
        })
    )

    password2 = forms.CharField(
        label="Ulangi Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Ulangi password',
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-blue transition'
        })
    )


    class Meta:
        model = CustomUser
        fields = ('email', )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False  
        if commit:
            user.save()
        return user

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['judul_buku', 'penulis_buku', 'bulan_baca', 'isi_review', 'cover_buku', 'gambar_infografis', 'link_video']
        widgets = {
            'bulan_baca': forms.DateInput(attrs={'type': 'month', 'class': 'border px-3 py-2 rounded w-full'}),
            'isi_review': forms.Textarea(attrs={'rows': 5, 'class': 'border px-3 py-2 rounded w-full'}),
            'judul_buku': forms.TextInput(attrs={'class': 'border px-3 py-2 rounded w-full'}),
            'penulis_buku': forms.TextInput(attrs={'class': 'border px-3 py-2 rounded w-full'}),
            'link_video': forms.URLInput(attrs={'class': 'border px-3 py-2 rounded w-full'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        gambar = cleaned_data.get("gambar_infografis")
        link = cleaned_data.get("link_video")
        isi = cleaned_data.get("isi_review")

        if not isi:
            raise forms.ValidationError("Review wajib diisi.")