from django.contrib import admin

from albums.models import Album, Artist, Track


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    search_fields = ["name"]


class TrackInline(admin.TabularInline):
    autocomplete_fields = ["track"]
    model = Album.tracks.through


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ["title", "artist", "year"]
    inlines = [TrackInline]
    search_fields = ["title", "artist__name"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("artist")


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    search_fields = ["title"]
