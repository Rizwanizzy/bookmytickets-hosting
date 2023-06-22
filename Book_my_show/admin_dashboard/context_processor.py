from home.models import UserProfile
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from room.models import *


def admin_side_messages(request):
    context = {}
    if request.user.is_superuser:
        chat_messages = (
            ChatMessage.objects.filter(recipient=request.user)
            .select_related("sender")
            .order_by("sender", "-id")
            .distinct("sender")
        )

        try:
            chat_messages_list = list(chat_messages)  # Convert queryset to list
            for message in chat_messages_list:
                sender = message.sender
                user_profile = UserProfile.objects.get(
                    user=sender
                )  # Retrieve the UserProfile for the sender
                print("username:", sender.username)
                print("profile image URL:", user_profile.profile_image.url)
            context = {"chat_messages": chat_messages_list}
        except ObjectDoesNotExist:
            pass
    return context
