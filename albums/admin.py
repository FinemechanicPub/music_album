from django.contrib import admin

from albums.models import Album, AlbumTrack, Artist, Track


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    pass


class TrackInline(admin.TabularInline):
    model = AlbumTrack


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ["title", "year"]
    inlines = [TrackInline]


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    pass
