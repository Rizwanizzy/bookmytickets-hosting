from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("all_movies/", views.all_movies, name="all_movies"),
    path("search/", views.search, name="search"),
    path("about/", views.about, name="about"),
    path("movie/<int:id>", views.movie, name="movie"),
    path("cinemas/", views.cinemas, name="cinemas"),
    path("list_movies/<int:id>/", views.list_movies, name="list_movies"),
    path("theatre_choose/<int:id>", views.theatre_choose, name="theatre_choose"),
    path(
        "seat_selection/<int:theatre_id>/<int:screen_id>/<int:show_time_id>/<str:selected_date>/",
        views.seat_selection,
        name="seat_selection",
    ),
    path("payment/", views.payment, name="payment"),
    path("payment_successful/", views.payment_successful, name="payment_successful"),
    path("user_logout/", views.user_logout, name="user_logout"),
]
