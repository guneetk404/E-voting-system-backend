from django.urls import path
from accounts import views
from rest_framework_simplejwt.views import (
    TokenVerifyView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/verify/', TokenVerifyView.as_view(), name='verify_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('blo/', views.BLOLogin.as_view(), name='BLOLogin'),
    path('voter1/', views.VOTERLoginStep1.as_view(), name='VOTERLogin1'),
    path('voter2/', views.VOTERLoginStep2.as_view(), name='VOTERLogin2'),
    path('admin/', views.ADMINLogin.as_view(), name='ADMINLogin'),
]
