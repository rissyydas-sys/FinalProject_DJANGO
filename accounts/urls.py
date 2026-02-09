from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    #path('register/', views.register, name='register'),
    # path('login/', TokenObtainPairView.as_view(), name='login'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('approve-user/<int:pk>/', views.ApproveUserView.as_view(), name='approve_user'),
    # path('admin-dashboard/', admin_dashboard, name='admin-dashboard'),
    path('user-approvals/', views.user_approvals, name='user-approvals'),
    path('add-course/', views.add_course, name='add-course'),
    path("login/", views.user_login, name="login"),
    path("dashboard/", views.user_dashboard, name="user-dashboard"),
    path("logout/", views.user_logout, name="logout"),
    path("approve-users/", views.approve_users, name="approve-users"),
    path("approve-user/<int:user_id>/", views.approve_user, name="approve-user"),
]
