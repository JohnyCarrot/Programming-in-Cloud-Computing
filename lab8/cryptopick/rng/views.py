import json
import secrets
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt


def health(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"status": "ok"})

@csrf_exempt
def pick(request: HttpRequest) -> JsonResponse:

    if request.method != "POST":
        return JsonResponse({"error": "POST method required."}, status=405)

    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON."}, status=400)

    items = payload.get("items", None)
    if not isinstance(items, list):
        return JsonResponse({"error": "'items' must be a JSON array."}, status=400)

    if len(items) == 0:
        return JsonResponse({"error": "'items' must not be empty."}, status=400)

    selected = items[secrets.randbelow(len(items))]

    return JsonResponse(selected)