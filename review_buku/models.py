from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email harus diisi")
        email = self.normalize_email(email)
        username = email.split('@')[0]
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.username:
            if self.email and self.email.endswith('@student.unsil.ac.id'):
                self.username = self.email.split('@')[0]
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.get_full_name() or self.username

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    judul_buku = models.CharField(max_length=200)
    penulis_buku = models.CharField(max_length=100)
    bulan_baca = models.CharField(max_length=7, help_text="Format: YYYY-MM")
    isi_review = models.TextField()

    cover_buku = models.ImageField(upload_to='cover_buku/', blank=True, null=True)
    gambar_infografis = models.ImageField(upload_to='infografis/', blank=True, null=True)
    link_video = models.URLField(blank=True, null=True)

    tanggal_submit = models.DateTimeField(auto_now_add=True)
    status_approve = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.judul_buku} oleh {self.user.username}"
