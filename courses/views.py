from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdminUser, IsRegularUser
from .models import Course, Enrollment
from .serializers import CourseSerializer, EnrollmentSerializer
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, "courses/course_list.html", {
        "courses": courses
    })


class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        return Enrollment.objects.filter(user=self.request.user)

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [IsAuthenticated, IsRegularUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


@login_required
def enroll_course(request, course_id):
    if not request.user.is_active:
        messages.warning(
            request,
            "Your account is waiting for admin approval."
        )
        return redirect("dashboard")

    if request.method == "POST":
        course = get_object_or_404(Course, id=course_id)
        Enrollment.objects.get_or_create(
            user=request.user,
            course=course
        )

    return redirect("courses:enrolled-courses")


@login_required
def enrolled_courses(request):
    enrollments = Enrollment.objects.filter(user=request.user)
    return render(request, "courses/enrolled_courses.html", {
        "enrollments": enrollments
    })

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # ✅ Ensure only enrolled users can watch
    enrolled = Enrollment.objects.filter(
        user=request.user,
        course=course
    ).exists()

    if not enrolled:
        return render(request, "courses/not_enrolled.html")

    return render(
        request,
        "courses/course_detail.html",
        {"course": course}
    )