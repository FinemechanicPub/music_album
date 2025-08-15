from django.test import Client
from django.urls import reverse
import pytest

pytestmark = pytest.mark.django_db

ERROR_COUNT = (
    "{method} request on {url} returned {actual} objects, "
    "while expected {expected}"
)
ERROR_NO_OBJECT = (
    "Object with id {id} not found in response to {method} request to {url}"
)

ERROR_OBJECT_FIELD = (
    "{method} request on {url} returned object {obj} with attribute"
    "atrr={attr}, while expected {expected}"
)


def check_enity(url, obj, data: dict, fields: list[str]):
    for field in fields:
        assert str(getattr(obj, field)) == str(data[field]), (
            ERROR_OBJECT_FIELD.format(
                method="GET",
                url=url,
                obj=obj,
                attr=field,
                expected=str(getattr(obj, field))
            )
        )


def group_by_id(results: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {
        result["id"]: {
            field: value for field, value in result.items() if field != "id"
            }
        for result in results
    }


def check_list_api(client: Client, objs, view: str, fields: list):
    url = reverse(view)
    response = client.get(url)
    count = response.data["count"]
    assert (
        count == len(objs)
    ), ERROR_COUNT.format(method="GET", url=url, actual=len(objs))
    data = group_by_id(response.data["results"])
    for obj in objs:
        assert str(obj.pk) in data, ERROR_NO_OBJECT.format(
            id=str(obj.pk), method="GET", url=url
        )
        check_enity(url, obj, data[str(obj.pk)], fields)


def test_track_list(client, tracks):
    check_list_api(
        client, objs=tracks, view="api:track-list", fields=["title"]
    )


def test_artist_list(client, artists):
    check_list_api(
        client, objs=artists, view="api:artist-list", fields=["name"]
    )


def test_album_list(client, albums):
    check_list_api(
        client,
        objs=albums,
        view="api:album-list",
        fields=["title", "year", "artist"]
    )
