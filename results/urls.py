from django.urls import path
from .views import results_list

urlpatterns = [
    path("", results_list, name="results"),
]
