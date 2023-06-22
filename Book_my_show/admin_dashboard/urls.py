from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path("admin_home/", views.admin_home, name="admin_home"),
    path("admin_profile/", views.admin_profile, name="admin_profile"),
    path("admin_movies", views.admin_movies, name="admin_movies"),
    path("add_movie", views.add_movie, name="add_movie"),
    path("update_movie/<int:id>", views.update_movie, name="update_movie"),
    path("delete_movie/<int:id>/", views.delete_movie, name="delete_movie"),
    path("admin_theatres", views.admin_theatres, name="admin_theatres"),
    path("admin_users", views.admin_users, name="admin_users"),
    path("block_user/<int:id>/", views.block_user, name="block_user"),
    path("unblock_user/<int:id>/", views.unblock_user, name="unblock_user"),
    path("block_theatre/<int:id>/", views.block_theatre, name="block_theatre"),
    path("unblock_theatre/<int:id>/", views.unblock_theatre, name="unblock_theatre"),
    path("admin_side_booking", views.admin_side_booking, name="admin_side_booking"),
    path("generate_excel/", views.generate_excel, name="generate_excel"),
    path(
        "admin_cancellation_requests",
        views.admin_cancellation_requests,
        name="admin_cancellation_requests",
    ),
    path("admin_logout/", views.admin_logout, name="admin_logout"),
]
