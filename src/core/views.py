from django.views.generic import RedirectView


class MoviesRedirectView(RedirectView):
    url = "/movies/"
