from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
#router.register(r'exams', views.ExamViewSet, basename='exam')

urlpatterns = [ # All routes handled automatically
    path('add-exam/', views.add_exam, name='add_exam'),
    path('exam-list/', views.exam_list, name='exam-list'),
    path('exams/<int:exam_id>/attend/', views.attend_exam, name='attend-exam'),
    path("exams/<int:exam_id>/result/", views.exam_result, name="exam-result"),
    path("result/<int:result_id>/", views.view_result, name="view_result"),
    path("history/", views.exam_history, name="exam_history"),
]
