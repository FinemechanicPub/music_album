import random
import pytest

from albums.models import Album, Artist, Track


@pytest.fixture
def tracks():
    TRACK_TITLE = "Track {n}"
    return [Track.objects.create(title=TRACK_TITLE.format(n=i)) for i in range(5)]


@pytest.fixture
def artists():
    ARTIST_NAME = "Artist {n}"
    return [Artist.objects.create(name=ARTIST_NAME.format(n=i)) for i in range(5)]


@pytest.fixture
def albums(artists, tracks):
    ALBUM_TITLE = "Album {n}"
    artist = artists[-1]
    albums = [
        Album.objects.create(
            title=ALBUM_TITLE.format(n=i),
            artist=artist,
            year=random.randint(1980, 2025),
        )
        for i in range(3)
    ]

    def add_tracks(album: Album, tracks: list[Track]):
        for i, track in enumerate(tracks, start=1):
            album.tracks.add(track, through_defaults={"position": i})

    n = len(tracks)
    add_tracks(albums[0], tracks[: n // 2])
    add_tracks(albums[1], tracks[n // 2 :])
    add_tracks(albums[2], tracks)
    return albums


@pytest.fixture
def artist_with_albums(albums):
    return albums[0].artist


@pytest.fixture
def albums_data(tracks, artists):
    album_data_1 = {
        "title": "New Album 1",
        "artist_id": str(artists[0].id),
        "year": 2030,
        "tracks": [
            {"id": str(tracks[0].id), "position": 1},
            {"id": str(tracks[1].id), "position": 2},
        ],
    }
    album_data_2 = {
        "title": "New Album 2",
        "artist_id": str(artists[1].id),
        "year": 2035,
        "tracks": [
            {"id": str(tracks[1].id), "position": 1},
            {"id": str(tracks[2].id), "position": 2},
        ],
    }
    return album_data_1, album_data_2
