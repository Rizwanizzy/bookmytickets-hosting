from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("theatre_home", views.theatre_home, name="theatre_home"),
    path("theatre_movies", views.theatre_movies, name="theatre_movies"),
    path("theatre_screen", views.theatre_screen, name="theatre_screen"),
    path("add_screen", views.add_screen, name="add_screen"),
    path("update_screen/<int:id>", views.update_screen, name="update_screen"),
    path("delete_screen/<int:id>", views.delete_screen, name="delete_screen"),
    path(
        "theatre_side_booking", views.theatre_side_booking, name="theatre_side_booking"
    ),
    path(
        "theatre_generate_excel",
        views.theatre_generate_excel,
        name="theatre_generate_excel",
    ),
    path(
        "cancellation_requests",
        views.cancellation_requests,
        name="cancellation_requests",
    ),
    path(
        "update_cancellation_request",
        views.update_cancellation_request,
        name="update_cancellation_request",
    ),
    path("theatre_profile", views.theatre_profile, name="theatre_profile"),
    path("theatre_logout/", views.theatre_logout, name="theatre_logout"),
]
