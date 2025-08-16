import json
from django.test import Client
from django.urls import reverse
import pytest

from albums.models import Album

pytestmark = pytest.mark.django_db


ERROR_COUNT = (
    "{method} request on {url} returned {actual} objects, " "while expected {expected}"
)
ERROR_NO_OBJECT = (
    "Object with id {id} not found in response to {method} request to {url}"
)

ERROR_OBJECT_FIELD = (
    "{method} request on {url} returned object '{obj}' with attribute "
    "'{attr}' = {actual}, while expected {expected}"
)

ERROR_OBJECT_INDENTITY = (
    "{method} request on {url} created object '{obj}' with "
    "id={id}, while expected {expected_id}"
)

ERROR_OBJECT_INDENTITIES = (
    "{method} request on {url} created a collection of objects "
    "with unexpected identities"
)

MISCONFIGURATION = (
    "Fixture model {model} has zero {related}. "
    "Did you forget to include 'albums' fixture?"
)


def check_entity(request: dict, obj, data: dict, fields: list[str]):
    method = request["REQUEST_METHOD"]
    url = request["PATH_INFO"]
    for field in fields:
        assert str(getattr(obj, field)) == str(data[field]), ERROR_OBJECT_FIELD.format(
            method=method,
            url=url,
            obj=obj,
            attr=field,
            actual=str(data[field]),
            expected=str(getattr(obj, field)),
        )


def group_by_id(results: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {
        result["id"]: {field: value for field, value in result.items() if field != "id"}
        for result in results
    }


def check_list_api(client: Client, objs, view: str, fields: list):
    url = reverse(view)
    response = client.get(url)
    count = response.data["count"]
    assert count == len(objs), ERROR_COUNT.format(
        method="GET", url=url, actual=len(objs), expected=count
    )
    data = group_by_id(response.data["results"])
    for obj in objs:
        assert str(obj.pk) in data, ERROR_NO_OBJECT.format(
            id=str(obj.pk), method="GET", url=url
        )
        check_entity(response.request, obj, data[str(obj.pk)], fields)


def test_track_list(client, tracks):
    check_list_api(client, objs=tracks, view="api:track-list", fields=["title"])


def test_artist_list(client, artists):
    check_list_api(client, objs=artists, view="api:artist-list", fields=["name"])


def test_album_list(client, albums):
    check_list_api(
        client, objs=albums, view="api:album-list", fields=["title", "year", "artist"]
    )


def test_track_get(client, tracks, albums):
    for track in tracks:
        url = reverse("api:track-detail", args=[track.pk])
        response = client.get(url)
        check_entity(response.request, track, response.data, ["id", "title"])
        response_albums = group_by_id(response.data["albums"])
        count = track.albumtrack_set.count()
        assert count > 0, MISCONFIGURATION.format(model="Track", related="AlbumTrack")
        for albumtrack in track.albumtrack_set.all():
            check_entity(
                response.request,
                albumtrack,
                response_albums[str(albumtrack.album_id)],
                ["position"],
            )


def test_artist_get(client, artists):
    for artist in artists:
        url = reverse("api:artist-detail", args=[artist.pk])
        response = client.get(url)
        check_entity(response.request, artist, response.data, ["id", "name"])


def test_artist_albums_get(client, artist_with_albums):
    url = reverse("api:artist-detail", args=[artist_with_albums.pk])
    response = client.get(url)
    response_albums = group_by_id(response.data["albums"])
    for album in artist_with_albums.albums.all():
        check_entity(response.request, album, response_albums[str(album.pk)], ["title"])


def test_album_get(client, albums):
    for album in albums:
        url = reverse("api:album-detail", args=[album.pk])
        response = client.get(url)
        check_entity(response.request, album, response.data, ["id", "title", "year"])
        artist = album.artist
        check_entity(
            response.request, artist, response.data["artist"], fields=["id", "name"]
        )
        response_tracks = group_by_id(response.data["tracks"])
        for albumtrack in album.albumtrack_set.all():
            response_track = response_tracks[str(albumtrack.track_id)]
            check_entity(response.request, albumtrack, response_track, ["position"])
            check_entity(response.request, albumtrack.track, response_track, ["title"])


def test_album_create(client, albums_data):
    album_data_1, album_data_2 = albums_data
    url = reverse("api:album-list")
    response = client.post(
        url, json.dumps(album_data_1), content_type="application/json"
    )
    new_id = response.data["id"]
    album_1 = Album.objects.get(pk=new_id)
    check_entity(response.request, album_1, album_data_1, fields=["title", "year"])
    db_id, expected_id = str(album_1.artist.id), album_data_1["artist_id"]
    assert db_id == expected_id, ERROR_OBJECT_INDENTITY.format(
        method="POST", url=url, obj=album_1.artist, id=db_id, expected_id=expected_id
    )
    assert set(str(track.id) for track in album_1.tracks.all()) == set(
        track["id"] for track in album_data_1["tracks"]
    ), ERROR_OBJECT_INDENTITIES.format(method="POST", url=url)
