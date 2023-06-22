from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, related_name="userprofile"
    )
    is_theatre = models.BooleanField(default=False)
    location = models.CharField(max_length=30)
    address = models.TextField()
    phone = PhoneNumberField(null=True, blank=True, unique=True, default=None)
    profile_image = models.ImageField(upload_to="profile_images/", null=True)

    def __str__(self):
        return str(self.user)
