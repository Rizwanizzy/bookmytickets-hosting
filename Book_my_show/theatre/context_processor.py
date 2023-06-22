from home.models import UserProfile
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


def theatre_profile_details(request):
    context = {}
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        try:
            theatre_user_profile = UserProfile.objects.get(user=user, is_theatre=True)
            context = {"theatre_user_profile": theatre_user_profile}
        except ObjectDoesNotExist:
            pass
    return context
