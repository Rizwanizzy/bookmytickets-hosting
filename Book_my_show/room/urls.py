from django.urls import path

from . import views

urlpatterns = [
    # User-side views
    path("", views.chatPage, name="chat-page"),
    path("save_chat_message/", views.save_chat_message, name="save_chat_message"),
    # Admin-side views
    path("admin/chat/<int:id>/", views.admin_chat_view, name="admin_chat"),
    path("admin/reply/", views.admin_reply_view, name="admin_reply"),
]
