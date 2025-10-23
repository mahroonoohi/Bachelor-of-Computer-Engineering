from django.urls import path, include

from users.views import LoginView, TokenRefreshView

urlpatterns = [
    path('auth/jwt/', include(([
        path('login/', LoginView.as_view(), name="login"),
        path('refresh/', TokenRefreshView.as_view(), name="refresh"),
    ])), name="jwt"),
]