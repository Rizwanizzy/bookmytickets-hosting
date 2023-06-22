from home.models import UserProfile
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


def user_profile_details(request):
    context = {}
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        try:
            user_profile = UserProfile.objects.get(user=user)
            context = {"user_profile": user_profile}
        except ObjectDoesNotExist:
            pass
    return context
