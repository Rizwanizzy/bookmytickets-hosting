from django.db import models
import datetime
from django.utils.translation import gettext as _

# from theatre.models import Theatre_Sale_Report

# Create your models here.


class All_Languages(models.Model):
    language = models.CharField(max_length=30)

    def __str__(self):
        return self.language


class Movies(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    cast = models.CharField(max_length=50, blank=True, null=True)
    director = models.CharField(max_length=50, null=True)
    writers = models.CharField(max_length=50, null=True)
    year = models.IntegerField(null=True)
    genre = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to="movie_images", blank=True)
    poster = models.ImageField(upload_to="movie_images", blank=True)
    release_date = models.DateField(_("Date"), default=datetime.date.today)
    language = models.ForeignKey(All_Languages, on_delete=models.CASCADE)
    trailer = models.URLField(max_length=300, blank=True)
    runtime = models.DurationField(blank=True, null=True)

    def __str__(self):
        return self.title
