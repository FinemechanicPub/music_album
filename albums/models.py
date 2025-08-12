from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid_utils.compat as uuid

TITLE_MAX_LENGTH = 200


class TimestampedBase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid7, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Artist(TimestampedBase):
    name = models.CharField(verbose_name=_("name"), max_length=TITLE_MAX_LENGTH)

    class Meta:
        verbose_name = _("artist")
        verbose_name_plural = _("artists")

    def __str__(self):
        return self.name


class Track(TimestampedBase):
    title = models.CharField(verbose_name=_("title"), max_length=TITLE_MAX_LENGTH)

    class Meta:
        verbose_name = _("track")
        verbose_name_plural = _("tracks")

    def __str__(self):
        return self.title


class Album(TimestampedBase):
    title = models.CharField(verbose_name=_("title"), max_length=TITLE_MAX_LENGTH)
    year = models.SmallIntegerField(verbose_name=_("year"))
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="albums")
    tracks = models.ManyToManyField(Track, through="AlbumTrack")

    class Meta:
        verbose_name = _("album")
        verbose_name_plural = _("albums")

    def __str__(self):
        return self.title


class AlbumTrack(TimestampedBase):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    position = models.PositiveSmallIntegerField(verbose_name=_("#"))

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["album", "position"], name="unique_track_position",
                violation_error_message=_("Each track in an album shall have its own unique position")
            )
        ]
        verbose_name = _("tracks for album")

    def __str__(self):
        return str(self.position)
