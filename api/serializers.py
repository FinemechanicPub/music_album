from rest_framework import serializers

from albums.models import Album, Artist, Track


class TrackAlbumsSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="album.id")

    class Meta:
        model = Album.tracks.through
        fields = ["id", "position"]


class TrackInAlbumSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="track.id")
    title = serializers.CharField(source="track.title")

    class Meta:
        model = Album.tracks.through
        fields = ["position", "id", "title"]


class TrackReferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Track
        fields = ["id", "title"]


class AlbumReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ["id", "title"]


class AlbumSerializer(serializers.ModelSerializer):
    artist = serializers.StringRelatedField()

    class Meta:
        model = Album
        fields = ["id", "title", "artist", "year"]


class AlbumDetailedSerializer(serializers.ModelSerializer):
    artist = serializers.StringRelatedField()
    tracks = TrackInAlbumSerializer(source="albumtrack_set", many=True)

    class Meta:
        model = Album
        fields = ["id", "title", "artist", "year", "tracks"]


class TrackDetailedSerializer(serializers.ModelSerializer):
    albums = TrackAlbumsSerializer(source="albumtrack_set", many=True)

    class Meta:
        model = Track
        fields = ["id", "title", "albums"]


class ArtistReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ["id", "name"]


class ArtistDetailedSerializer(serializers.ModelSerializer):
    albums = AlbumReferenceSerializer(many=True)

    class Meta:
        model = Artist
        fields = ["id", "name", "albums"]
