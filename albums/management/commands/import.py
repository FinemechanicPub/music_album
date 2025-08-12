import json
from django.core.management.base import BaseCommand, CommandError

from albums.models import Album, Artist, Track

EXPECTED_FIELDS = set(("title", "artist", "year", "tracks"))


class Command(BaseCommand):
    help = "Imports albums from a json file"

    def add_arguments(self, parser):
        parser.add_argument("filename", type=str)

    def handle(self, *args, **options):
        with open(options["filename"], "r", encoding="utf8") as file:
            data = json.load(file)
            if "albums" not in data or not isinstance(data["albums"], list):
                raise CommandError("JSON shall contain 'albums' list")
            for import_album in data["albums"]:
                if (
                    not isinstance(import_album, dict)
                    or EXPECTED_FIELDS < import_album.keys()
                ):
                    raise CommandError(
                        "Each album is expected to have "
                        "'title', 'artist', 'year' and 'tracks' fields"
                    )
                title = import_album["title"]
                artist_name = import_album["artist"]
                year = import_album["year"]
                artist, _ = Artist.objects.get_or_create(name=artist_name)
                album = Album.objects.create(title=title, artist=artist, year=year)
                for position, track_title in enumerate(import_album["tracks"], start=1):
                    track, _ = Track.objects.get_or_create(title=track_title)
                    album.tracks.add(track, through_defaults={"position": position})
