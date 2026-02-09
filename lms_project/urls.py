from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.home, name='home'),

    # Admin site and admin login/logout
    path('admin/', admin.site.urls),

    # User auth
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

 path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('register/', views.user_register, name='register'),
    path("registration-pending/", views.registration_pending, name="registration-pending"),

    # User dashboard
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),

    # API endpoints for courses, exams, etc.
    path('api/accounts/', include('accounts.urls')),
    path('api/', include('courses.urls')),
    path('api/exams/', include('exams.urls')),
    path("results/", include("results.urls")),
    path("certificate/", include("certificates.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )