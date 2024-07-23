from django.urls import path

from .views import MenuDetail, MenuList

urlpatterns = [
    path("", MenuList.as_view(), name="subscription-list"),
    path("<int:pk>/", MenuDetail.as_view(), name="subscription-detail"),
]
