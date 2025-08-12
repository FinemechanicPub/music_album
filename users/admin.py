from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AlbumUser

admin.site.register(AlbumUser, UserAdmin)
