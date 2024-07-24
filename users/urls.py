from django.urls import path
from . import views

urlpatterns = [
    path('kakao/login/', views.kakao_login, name='kakao_login'),
    path('kakao/callback/', views.kakao_callback, name='kakao_callback'),
    path('kakao/logout/', views.kakao_logout, name='kakao_logout'),
]