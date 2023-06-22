from django.db import models
from home.models import *
from theatre.models import *
from admin_dashboard.models import *

# Create your models here.


class BookingCancellationRequest(models.Model):
    booking = models.ForeignKey(BookedSeat, on_delete=models.CASCADE)
    theatre = models.CharField(max_length=50, default=None)
    user = models.CharField(max_length=50, default=None)
    reason = models.TextField(default=None)
    status = models.CharField(
        max_length=10,
        choices=(
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("declined", "Declined"),
        ),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.booking)
