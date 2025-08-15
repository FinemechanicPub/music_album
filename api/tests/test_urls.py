from django.urls import reverse
from http import HTTPStatus
import pytest

pytestmark = pytest.mark.django_db

WRONG_STATUS = (
    "A {method} request to {url} returned {status}, expected {expected}"
)


@pytest.mark.parametrize(
        ["url", "expected"],
        [
            (reverse("api:track-list"), HTTPStatus.OK),
            (reverse("api:artist-list"), HTTPStatus.OK),
            (reverse("api:album-list"), HTTPStatus.OK),
        ]
)
def test_get_response(client, url, expected):
    status = client.get(url).status_code
    assert status == expected, WRONG_STATUS.format(
        method="GET", url=url, status=status, expected=expected
    )
