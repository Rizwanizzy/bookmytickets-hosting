from django.contrib import admin
from .models import *

# Register your models here.


class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "genre", "release_date", "language", "runtime")


admin.site.register(All_Languages)
admin.site.register(Movies, MovieAdmin)
