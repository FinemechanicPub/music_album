from rest_framework import viewsets

from albums.models import Album, Artist, Track
from api.filters import AlbumFilter, TrackFilter
from api.serializers import (
    AlbumSerializer,
    AlbumDetailedSerializer,
    ArtistDetailedSerializer,
    ArtistReferenceSerializer,
    TrackDetailedSerializer,
    TrackReferenceSerializer,
)


class AlbumViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Album.objects.select_related("artist").order_by("title")
    serializer_class = AlbumSerializer
    filterset_class = AlbumFilter

    def get_queryset(self):
        if self.action == "retrieve":
            return super().get_queryset().prefetch_related("albumtrack_set__track")
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action != "list":
            return AlbumDetailedSerializer
        return super().get_serializer_class()


class ArtistViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Artist.objects.order_by("name")
    serializer_class = ArtistReferenceSerializer

    def get_serializer_class(self):
        if self.action != "list":
            return ArtistDetailedSerializer
        return super().get_serializer_class()


class TrackViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Track.objects.order_by("title")
    serializer_class = TrackReferenceSerializer
    filterset_class = TrackFilter

    def get_queryset(self):
        if self.action == "retrieve":
            return super().get_queryset().prefetch_related("albumtrack_set__album")
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action != "list":
            return TrackDetailedSerializer
        return super().get_serializer_class()
