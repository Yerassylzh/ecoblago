from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def view(request: HttpRequest) -> HttpResponse:
    return render(request, "policy/terms_of_usage.html")
