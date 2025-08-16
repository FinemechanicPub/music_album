from rest_framework import serializers

from albums.models import Album, Artist, Track


class TrackAlbumsSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="album.id")

    class Meta:
        model = Album.tracks.through
        fields = ["id", "position"]


class TrackInAlbumSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="track_id")
    title = serializers.CharField(source="track.title", read_only=True)

    class Meta:
        model = Album.tracks.through
        fields = ["id", "title", "position"]


class TrackReferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Track
        fields = ["id", "title"]


class ArtistReferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = ["id", "name"]
        read_only_fields = ["name"]


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
    artist = ArtistReferenceSerializer(read_only=True)
    artist_id = serializers.PrimaryKeyRelatedField(
        write_only=True, source="artist", queryset=Artist.objects.all()
    )
    tracks = TrackInAlbumSerializer(source="albumtrack_set", many=True)

    def create(self, validated_data):
        album_tracks_data = (
            validated_data.pop("albumtrack_set")
            if "albumtrack_set" in validated_data
            else {}
        )
        instance = super().create(validated_data)
        for track_data in album_tracks_data:
            instance.albumtrack_set.create(**track_data)
        return instance

    def update(self, instance, validated_data):
        album_tracks_data = (
            validated_data.pop("albumtrack_set")
            if "albumtrack_set" in validated_data
            else {}
        )
        instance = super().update(instance, validated_data)
        instance.albumtrack_set.all().delete()
        for track_data in album_tracks_data:
            instance.albumtrack_set.create(**track_data)
        return instance

    class Meta:
        model = Album
        fields = ["id", "title", "artist", "artist_id", "year", "tracks"]


class TrackDetailedSerializer(serializers.ModelSerializer):
    albums = TrackAlbumsSerializer(source="albumtrack_set", many=True, read_only=True)

    class Meta:
        model = Track
        fields = ["id", "title", "albums"]


class ArtistDetailedSerializer(serializers.ModelSerializer):
    albums = AlbumReferenceSerializer(many=True, read_only=True)

    class Meta:
        model = Artist
        fields = ["id", "name", "albums"]
