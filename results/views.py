from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def results_list(request):
    # later we will fetch real results from DB
    return render(request, "results/results_list.html")
