from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

# Create your views here.


def chatPage(request, *args, **kwargs):
    admin = User.objects.get(username="admin")
    if request.method == "POST":
        pass
    chat_messages = ChatMessage.objects.filter(
        sender=request.user, recipient=admin
    ) | ChatMessage.objects.filter(sender=admin, recipient=request.user)

    return render(request, "room/chatPage.html", {"chat_messages": chat_messages})


def admin_chat_view(request, id):
    user = User.objects.get(id=id)
    admin = request.user

    if request.method == "POST":
        message = request.POST.get("message")
        sender = request.user
        recipient = user
        print("message:", message, "sender:", sender, "recipient:", recipient)
        # Create a new ChatMessage instance and save it to the database
        chat_message = ChatMessage(message=message, sender=sender, recipient=recipient)
        chat_message.save()
        return redirect("admin_chat", id=id)

    chat_messages = ChatMessage.objects.filter(
        sender=admin, recipient=user
    ) | ChatMessage.objects.filter(sender=user, recipient=admin)
    return render(
        request,
        "room/admin_chat.html",
        {"chat_messages": chat_messages, "user_id": user},
    )


def admin_reply_view(request):
    if request.method == "POST":
        message = request.POST.get("message")
        sender = request.user
        recipient = request.POST.get("recipient")
        print("message", message, "sender", sender, "recipient", recipient)
        # Create a new ChatMessage instance and save it to the database
        chat_message = ChatMessage(message=message, sender=sender, recipient=recipient)
        chat_message.save()

        return redirect("admin_chat")  # Redirect back to the admin chat view

    return render(request, "room/admin_reply.html")


@csrf_exempt
def save_chat_message(request):
    if request.method == "POST":
        message = request.POST.get("message")
        sender = request.POST.get("sender")
        recipient = request.POST.get("recipient")

        print("this is save chat message here :", message, sender, recipient)
        user = User.objects.get(username=sender)
        admin = User.objects.get(username="admin")
        # Create a new ChatMessage instance and save it to the database
        chat_message = ChatMessage(message=message, sender=user, recipient=admin)
        chat_message.save()

        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "error"})
