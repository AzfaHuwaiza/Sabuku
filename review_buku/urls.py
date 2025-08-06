from django.urls import path
from django.conf import settings
from django.views.generic import TemplateView
from django.conf.urls.static import static
from .views import *
from .controller.auth import *

urlpatterns = [
    path('', home, name='home'),
    path('accounts/register/', register_view, name='register'),
    path('accounts/login/', login_view, name='login'),
    path('accounts/logout/', logout_view, name='logout'),
    path('my-page/', my_page, name='my_page'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate'),
    path('galeri-review/', galeri_review, name='galeri_review'),
    path('submit-review/', submit_review, name='submit_review'),
    path('edit-review/', edit_review, name='edit_review'),
    path('delete-review/', delete_review, name='delete_review'),
    path('isi-nama/', isi_nama, name='isi_nama'),
    path('review-management/', admin_approval_page, name='admin_approval_page'),
    path('review/approve/<int:review_id>/', approve_review, name='approve_review'),
]