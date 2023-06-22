from django.urls import path

from . import views

urlpatterns = [
    path("", views.chat_user_home, name="chat_user_home"),
]
