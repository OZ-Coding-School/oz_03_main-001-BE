from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.urls import path, include
from . import views


def hello_test(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Hello World")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("hello/", hello_test),
    path("api/v1/users/", include("oauth.urls")),
    path("api/v1/users/", include("users.urls")),
    path("", views.index, name="/"),
]
