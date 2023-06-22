from django.db import models
from django.contrib.auth.models import User
from admin_dashboard.models import Movies
from home.models import *
from django.utils import timezone
from datetime import datetime
import uuid
from .models import *

# Create your models here.


class Show_Time(models.Model):
    time = models.TimeField()

    def __str__(self):
        time_obj = datetime.strptime(self.time, "%H:%M:%S").time()
        return time_obj.strftime("%I:%M%p")


class Screen(models.Model):
    theatre = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    price1 = models.DecimalField(max_digits=6, decimal_places=2)
    price2 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    price3 = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    movies = models.ForeignKey(Movies, on_delete=models.CASCADE)
    show_times = models.ManyToManyField(Show_Time)
    total_seat_rows = models.IntegerField(default=None)
    total_seat_columns = models.IntegerField(default=None)

    def __str__(self) -> str:
        return f"{self.name} - {self.theatre.user}"


def get_default_booked_time():
    return timezone.now().time()


def get_default_booked_date():
    return timezone.now().date()


class BookedSeat(models.Model):
    booking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.CharField(max_length=255, default=None)
    movie = models.CharField(max_length=30, default=None)
    movie_poster = models.ImageField(upload_to="booked_movie_images", blank=True)
    email = models.EmailField(max_length=50)
    phone = PhoneNumberField(null=True, blank=False, default=None)
    theatre = models.CharField(max_length=255, default=None)
    screen = models.CharField(max_length=255, default=None)
    booked_seats = models.CharField(max_length=255, default=None)
    count = models.PositiveIntegerField(default=0)
    price = models.IntegerField(default=None)
    date = models.CharField(max_length=20)
    show_time = models.CharField(max_length=255, default="")
    payment_order_id = models.CharField(max_length=100, default=None)
    payment_id = models.CharField(max_length=100, default=None, null=True)
    booked_date = models.DateField(default=get_default_booked_date)
    booked_time = models.TimeField(default=get_default_booked_time)

    def set_booked_seats(self, integer_list):
        self.booked_seats = ",".join(str(i) for i in integer_list)

    def get_booked_seats(self):
        return [int(i) for i in self.booked_seats.split(",")]

    def __str__(self):
        return str(self.booking_id)


class Theatre_Sale_Report(models.Model):
    name = models.CharField(max_length=255, default=None)
    booking = models.ForeignKey(BookedSeat, on_delete=models.CASCADE)
    theatre_earnings = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Admin_Sale_Report(models.Model):
    name = models.CharField(max_length=255, default=None)
    theatre_sale_report = models.ForeignKey(
        Theatre_Sale_Report, on_delete=models.CASCADE
    )
    admin_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name
