from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from . import views
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


def hello_test(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Hello World")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("v1/schema", SpectacularAPIView.as_view(), name="schema"),
    path("v1/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger_ui"),
    path("v1/schema/redoc/", SpectacularSwaggerView.as_view(url_name="schema"), name="redoc"),
    path("hello/", hello_test),
    path("api/v1/users/", include("oauth.urls")),
    path("api/v1/users/", include("users.urls")),
    path("", views.index, name="/"),
    path("v1/menus/", include("menus.urls")),
    path("v1/lunch/", include("lunch.urls")),
    path("v1/orders/", include("orders.urls")),

]
