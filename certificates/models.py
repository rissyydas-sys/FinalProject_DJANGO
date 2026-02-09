from django.db import models
from django.contrib.auth.models import User
from exams.models import ExamResult


class Certificate(models.Model):
    result = models.OneToOneField(
        ExamResult,
        on_delete=models.CASCADE
    )
    issued_at = models.DateTimeField(auto_now_add=True)
    certificate_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Certificate {self.certificate_id}"
