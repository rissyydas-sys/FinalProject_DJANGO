from rest_framework import serializers
from .models import Exam

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'  # or list fields you want to expose, e.g., ['id', 'title', 'description', 'start_time', 'end_time']
