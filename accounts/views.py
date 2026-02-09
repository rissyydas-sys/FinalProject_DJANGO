from rest_framework import generics, permissions
from rest_framework.response import Response

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from courses.forms import CourseForm
from .serializers import RegisterSerializer
from django.contrib.admin.views.decorators import staff_member_required

# ✅ Correct way to use custom user model
User = get_user_model()


# ============================
# DRF REGISTER USER API
# ============================
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


# ============================
# DRF APPROVE USER API
# ============================
class ApproveUserView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({"message": "User approved successfully"})


# ============================
# ADMIN CHECK
# ============================
def is_admin(user):
    return user.is_superuser


# # ============================
# # ADMIN DASHBOARD
# # ============================
# @user_passes_test(is_admin)
# def admin_dashboard(request):
#     context = {
#         'pending_users': User.objects.filter(is_active=False).count(),
#         'course_count': Course.objects.count(),
#         'exam_count': Exam.objects.count(),
#     }
#     return render(request, 'admin/dashboard.html', context)


# ============================
# USER APPROVAL LIST
# ============================
@user_passes_test(is_admin)
def user_approvals(request):
    users = User.objects.filter(is_active=False)
    return render(request, 'admin/user_approvals.html', {'users': users})


# ============================
# APPROVE USER (FRONTEND)
# ============================
@staff_member_required
def approve_users(request):
    users = User.objects.filter(is_active=False)
    return render(request, "admin/approve_users.html", {
        "users": users
    })


@staff_member_required
def approve_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    return redirect("approve-users")


# ============================
# ADD COURSE
# ============================
@user_passes_test(is_admin)
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin-dashboard')
    else:
        form = CourseForm()

    return render(request, 'admin/add_course.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(username=username)
            if not user_obj.is_active:
                return render(request, "registration/login.html", {
                    "error": "Your account is pending admin approval."
                })
        except User.DoesNotExist:
            pass

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")

        return render(request, "registration/login.html", {
            "error": "Invalid username or password"
        })

    return render(request, "registration/login.html")


@login_required
def user_dashboard(request):
    return render(request, "accounts/dashboard.html")


@login_required
def user_logout(request):
    logout(request)
    return redirect("login")

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Account created successfully. Please login.")
        return redirect("login")   # ✅ REDIRECT TO LOGIN PAGE

    return render(request, "registration/register.html")