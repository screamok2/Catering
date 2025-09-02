from django.contrib import admin
from django.urls import path, include
from users.views import UserRegisterView, activate_user
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("admin/food/dish/import-dishes/", include('food.urls')),  # Можно оставить import_dishes отдельно
    path('food/', include('food.urls')),  # все маршруты food/*

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('registration/', UserRegisterView.as_view(), name='user-register'),
    path("activate/<uuid:code>/", activate_user, name="activate-user"),
]
