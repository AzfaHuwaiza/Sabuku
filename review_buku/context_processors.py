from .models import Review

def review_pending_count(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return {
            'review_pending_count': Review.objects.filter(status_approve=False).count()
        }
    return {}
