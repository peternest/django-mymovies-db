from django.views.generic import RedirectView


class UnusedMoviesRedirectView(RedirectView):
    url = "/movies/"
