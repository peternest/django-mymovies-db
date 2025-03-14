from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

from core.views import HomePageView

urlpatterns = [
    path("movies/", include("apps.movies.urls")),
    path("admin/", admin.site.urls),
    path("", HomePageView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
