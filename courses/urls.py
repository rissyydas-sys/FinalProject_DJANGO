from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = "courses"
urlpatterns = [
   path('api/course-list/', views.course_list, name='course-list'),
    path('api/enroll/<int:course_id>/', views.enroll_course, name='enroll-course'),
    path('api/enrolled-courses/', views.enrolled_courses, name='enrolled-courses'),
    path(
        "course/<int:course_id>/",
        views.course_detail,
        name="course_detail"
    ),
]
