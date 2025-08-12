from django.contrib import admin

from albums.models import Album, AlbumTrack, Artist


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    pass


class TrackInline(admin.TabularInline):
    model = AlbumTrack


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ["title", "year"]
    inlines = [TrackInline]
