from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from . import views
# TODO dosirock/views.py 삭제하고 path("", views.index, name="/"), 이 부분 변경


def hello_test(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Hello World")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("v1/schema", SpectacularAPIView.as_view(), name="schema"),
    path("v1/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger_ui"),
    path("v1/schema/redoc/", SpectacularSwaggerView.as_view(url_name="schema"), name="redoc"),
    path("hello/", hello_test),
    path("v1/users/", include("oauth.urls")),
    path("v1/users/", include("users.urls")),
    path("", views.index, name="/"),
    path("v1/menus/", include("menus.urls")),
    path("v1/lunch/", include("lunch.urls")),
    path("v1/orders/", include("orders.urls")),
]
