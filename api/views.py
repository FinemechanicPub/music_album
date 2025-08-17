from drf_spectacular.utils import extend_schema
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


@extend_schema(tags=["Album"])
class AlbumViewset(viewsets.ModelViewSet):
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


@extend_schema(tags=["Artist"])
class ArtistViewset(viewsets.ModelViewSet):
    queryset = Artist.objects.order_by("name")
    serializer_class = ArtistReferenceSerializer

    def get_serializer_class(self):
        if self.action != "list":
            return ArtistDetailedSerializer
        return super().get_serializer_class()


@extend_schema(tags=["Track"])
class TrackViewset(viewsets.ModelViewSet):
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
