from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView


urlpatterns = [
    path("", RedirectView.as_view(url="/movies/")),
    path("admin/", admin.site.urls),
    path("movies/", include("apps.movies.urls")),
    path("api/", include("apps.movies.urls_api")),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
]
