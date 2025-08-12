from django.urls import include, path
from rest_framework import routers

from api import views


router_v1 = routers.DefaultRouter()
router_v1.register("albums", views.AlbumViewset, basename="album")
router_v1.register("artists", views.ArtistViewset, basename="artist")
router_v1.register("tracks", views.TrackViewset, basename="track")

urlpatterns = [
    path("v1/", include(router_v1.urls)),
]
