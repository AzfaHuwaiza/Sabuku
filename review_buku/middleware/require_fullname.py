from django.shortcuts import redirect
from django.urls import reverse

class RequireFullNameMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_paths = [
            reverse('login'),
            reverse('logout'),
            reverse('isi_nama'),
        ]
        if request.path in allowed_paths or request.path.startswith('/admin'):
            return self.get_response(request)

        user = request.user
        if user.is_authenticated and (not user.first_name):
            request.show_fill_name_modal = True  
        else:
            request.show_fill_name_modal = False

        response = self.get_response(request)
        return response
