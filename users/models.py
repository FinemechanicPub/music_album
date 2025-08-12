from django.contrib.auth.models import AbstractUser
from django.db.models import UUIDField
import uuid_utils.compat as uuid


class AlbumUser(AbstractUser):
    id = UUIDField(primary_key=True, default=uuid.uuid7, editable=False)
