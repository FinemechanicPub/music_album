from django_filters import rest_framework as filter

from albums.models import Album, Artist, Track


class AlbumFilter(filter.FilterSet):
    title = filter.CharFilter(lookup_expr="icontains")
    artist = filter.CharFilter(field_name="artist__name", lookup_expr="icontains")
    year = filter.RangeFilter()

    class Meta:
        model = Album
        fields = ["title", "artist"]


class ArtistFilter(filter.FilterSet):
    name = filter.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Artist
        fields = ["name"]


class TrackFilter(filter.FilterSet):
    title = filter.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Track
        fields = ["title"]
