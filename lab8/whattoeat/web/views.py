import os
from django.http import JsonResponse, HttpRequest
from django.shortcuts import render


MEAL_PICKER_URL = os.getenv("MEAL_PICKER_URL", "http://127.0.0.1:8000")


def index(request: HttpRequest):
    return render(request, "index.html", {"MEAL_PICKER_URL": MEAL_PICKER_URL})


def health(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"status": "ok"})
