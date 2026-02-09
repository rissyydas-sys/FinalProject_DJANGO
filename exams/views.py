from django.shortcuts import render, redirect, get_object_or_404
from .models import Exam, ExamResult, Question
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def exam_list(request):
    exams = Exam.objects.all()
    return render(request, "exams/exam_list.html", {"exams": exams})


@login_required
def attend_exam(request, exam_id):
    if not request.user.is_active:
        messages.warning(
            request,
            "Your account is waiting for admin approval."
        )
        return redirect("dashboard")
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.questions.all()

    if request.method == "POST":
        score = 0

        for q in questions:
            selected = request.POST.get(f"q{q.id}")
            if selected and int(selected) == q.correct_option:
                score += 1

        total = questions.count()
        percentage = (score / total) * 100 if total > 0 else 0
        passed = percentage >= 40

        result = ExamResult.objects.create(
            student=request.user,
            exam=exam,
            score=score,
            total_questions=total,
            percentage=percentage,
            passed=passed
        )

        return redirect("view_result", result.id)

    return render(request, "exams/attend_exam.html", {
        "exam": exam,
        "questions": questions
    })




def add_exam(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")

        exam = Exam.objects.create(
            title=title,
            description=description
        )

        questions = request.POST.getlist("question[]")
        option1 = request.POST.getlist("option1[]")
        option2 = request.POST.getlist("option2[]")
        option3 = request.POST.getlist("option3[]")
        option4 = request.POST.getlist("option4[]")
        correct = request.POST.getlist("correct[]")

        for i in range(len(questions)):
            Question.objects.create(
                exam=exam,
                question_text=questions[i],
                option1=option1[i],
                option2=option2[i],
                option3=option3[i],
                option4=option4[i],
                correct_option=correct[i],
            )
        messages.success(request, "Exam created successfully!")
        return redirect("add_exam")

    return render(request, "admin/add_exam.html")


@login_required
def exam_result(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    # Get latest attempt of this user for this exam
    attempt = ExamResult.objects.filter(
        user=request.user,
        exam=exam
    ).order_by("-attempted_on").first()

    if not attempt:
        return render(request, "exams/no_result.html", {"exam": exam})

    percentage = (attempt.score / exam.total_marks) * 100
    passed = percentage >= 40  # you can change pass percentage

    context = {
        "exam": exam,
        "attempt": attempt,
        "percentage": round(percentage, 2),
        "passed": passed,
    }

    return render(request, "exams/exam_result.html", context)

@login_required
def view_result(request, result_id):
    result = get_object_or_404(ExamResult, id=result_id, student=request.user)
    return render(request, "exams/view_result.html", {"result": result})

@login_required
def exam_history(request):
    results = ExamResult.objects.filter(student=request.user)
    return render(request, "exams/exam_history.html", {"results": results})