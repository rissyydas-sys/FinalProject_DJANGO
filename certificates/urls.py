from django.urls import path
from . import views

app_name = "certificates"   # 🔴 VERY IMPORTANT

urlpatterns = [
    path(
        "",
        views.certificate_dashboard,
        name="dashboard"
    ),
     path(
        "download/<int:result_id>/",
        views.download_certificate,
        name="download"
    ),
]
