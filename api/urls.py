from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from rest_framework import routers

from api import views

app_name = "api"

router_v1 = routers.DefaultRouter()
router_v1.register("albums", views.AlbumViewset, basename="album")
router_v1.register("artists", views.ArtistViewset, basename="artist")
router_v1.register("tracks", views.TrackViewset, basename="track")

urlpatterns = [
    path("v1/", include(router_v1.urls)),
    path("v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "v1/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name=f"{app_name}:schema"),
        name="swagger-ui",
    ),
]
