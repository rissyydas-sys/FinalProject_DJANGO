from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from accounts.forms import RegisterForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from courses.models import Course
from exams.models import Exam
from django.contrib import messages
User = get_user_model()

def home(request):
    return render(request, 'home.html')

@login_required
def user_dashboard(request):
    if request.user.is_staff or request.user.is_superuser:
        return redirect('/admin/dashboard/')  # or /admin/
    return render(request, 'user_dashboard.html')


def user_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # ✅ CHECK if username already exists
        if User.objects.filter(username=username).exists():
            return render(request, "registration/register.html", {
                "error": "Username already exists. Please choose another one."
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.is_active = False  # waiting for admin approval
        user.save()

        return redirect("registration-pending")

    return render(request, "registration/register.html")


def is_admin(user):
    return user.is_superuser


# ============================
# ADMIN DASHBOARD
# ============================
@user_passes_test(is_admin)
def admin_dashboard(request):
    context = {
        'pending_users': User.objects.filter(is_active=False).count(),
        'course_count': Course.objects.count(),
        'exam_count': Exam.objects.count(),
    }
    return render(request, 'admin/dashboard.html', context)

def registration_pending(request):
    return render(request, "registration_pending.html")