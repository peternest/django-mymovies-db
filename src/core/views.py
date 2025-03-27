from django.shortcuts import render
# from django.views.generic import RedirectView


# class HomePageView(RedirectView):
#     url = "/movies/top100/"


def index(request):
    return render(request, "core/index.html")
