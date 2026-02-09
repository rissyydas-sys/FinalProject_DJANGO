import uuid
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas

from .models import Certificate
from exams.models import ExamResult

@login_required
def certificate_dashboard(request):
    results = ExamResult.objects.filter(
        student=request.user
    ).select_related("exam")

    passed_results = results.filter(passed=True)

    return render(
        request,
        "certificates/dashboard.html",
        {
            "results": results,
            "passed_results": passed_results,
        }
    )


@login_required
def download_certificate(request, result_id):
    result = get_object_or_404(
        ExamResult,
        id=result_id,
        student=request.user,
        passed=True
    )

    certificate, created = Certificate.objects.get_or_create(
        result=result,
        defaults={
            "certificate_id": str(uuid.uuid4())
        }
    )

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="certificate_{certificate.certificate_id}.pdf"'
    )

    pdf = canvas.Canvas(response)
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(300, 750, "Certificate of Achievement")

    pdf.setFont("Helvetica", 14)
    pdf.drawCentredString(
        300, 700,
        f"This certifies that {result.student.username}"
    )
    pdf.drawCentredString(
        300, 670,
        f"has successfully passed the exam"
    )
    pdf.drawCentredString(
        300, 640,
        f"'{result.exam.title}'"
    )

    pdf.drawString(50, 100, f"Certificate ID: {certificate.certificate_id}")
    pdf.drawString(50, 80, f"Issued On: {certificate.issued_at.date()}")

    pdf.showPage()
    pdf.save()

    return response

