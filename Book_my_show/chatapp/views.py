from django.shortcuts import render
from .models import *


# Create your views here.
def chat_user_home(request):
    return render(request, "chatapp/chat_user_home.html")
