import os
import requests

from django.http import JsonResponse, HttpRequest


ALLOWED_TAGS = ["cheap", "meat", "vegetarian", "vegan", "fish"]


MEALS = [
    {"name": "Pasta aglio e olio", "tags": ["cheap", "vegetarian"]},
    {"name": "Tomato basil pasta", "tags": ["cheap", "vegetarian"]},
    {"name": "Lentil soup", "tags": ["cheap", "vegan"]},
    {"name": "Chickpea curry", "tags": ["vegan"]},
    {"name": "Vegetable stir-fry with rice", "tags": ["cheap", "vegan"]},
    {"name": "Veggie fried rice", "tags": ["cheap", "vegan"]},
    {"name": "Peanut noodles", "tags": ["cheap", "vegan"]},
    {"name": "Bean burrito", "tags": ["cheap", "vegan"]},
    {"name": "Falafel wrap", "tags": ["vegan"]},
    {"name": "Hummus bowl with veggies", "tags": ["vegan"]},
    {"name": "Veggie chili", "tags": ["cheap", "vegan"]},
    {"name": "Mushroom risotto", "tags": ["vegetarian"]},
    {"name": "Caprese salad", "tags": ["vegetarian"]},
    {"name": "Cheese omelette", "tags": ["vegetarian"]},
    {"name": "Spinach feta quiche", "tags": ["vegetarian"]},
    {"name": "Margherita pizza", "tags": ["vegetarian"]},
    {"name": "Grilled cheese sandwich", "tags": ["cheap", "vegetarian"]},
    {"name": "Veggie quesadilla", "tags": ["vegetarian"]},
    {"name": "Potato pancakes", "tags": ["cheap", "vegetarian"]},
    {"name": "Pasta pesto", "tags": ["vegetarian"]},

    {"name": "Chicken stir-fry", "tags": ["meat"]},
    {"name": "Beef tacos", "tags": ["meat"]},
    {"name": "Pork schnitzel", "tags": ["meat"]},
    {"name": "Meatballs in tomato sauce", "tags": ["meat"]},
    {"name": "Chicken curry", "tags": ["meat"]},
    {"name": "Beef burger", "tags": ["meat"]},
    {"name": "Pulled pork sandwich", "tags": ["meat"]},
    {"name": "Sausage with potatoes", "tags": ["meat", "cheap"]},
    {"name": "Roast chicken with potatoes", "tags": ["meat"]},
    {"name": "Spaghetti bolognese", "tags": ["meat"]},

    {"name": "Tuna salad", "tags": ["fish"]},
    {"name": "Salmon with rice", "tags": ["fish"]},
    {"name": "Fish tacos", "tags": ["fish"]},
    {"name": "Shrimp pasta", "tags": ["fish"]},
    {"name": "Sardines on toast", "tags": ["fish", "cheap"]},
    {"name": "Mackerel salad", "tags": ["fish"]},
    {"name": "Fish and chips", "tags": ["fish"]},
    {"name": "Sushi bowl (simple)", "tags": ["fish"]},
    {"name": "Seafood paella", "tags": ["fish"]},
    {"name": "Clam spaghetti", "tags": ["fish"]},

    {"name": "Vegan ramen", "tags": ["vegan"]},
    {"name": "Tofu stir-fry", "tags": ["vegan"]},
    {"name": "Vegan salad bowl", "tags": ["vegan"]},
    {"name": "Vegan pasta primavera", "tags": ["vegan"]},
    {"name": "Vegetable soup", "tags": ["cheap", "vegetarian"]},
    {"name": "Vegetarian lasagna", "tags": ["vegetarian"]},
    {"name": "Kebab wrap", "tags": ["meat"]},
    {"name": "Fish soup", "tags": ["fish", "cheap"]},
    {"name": "Vegan burrito bowl", "tags": ["cheap", "vegan"]},
    {"name": "Couscous salad", "tags": ["vegetarian"]},
]

CRYPTOPICK_URL = os.getenv("CRYPTOPICK_URL", "http://127.0.0.1:8001")


def health(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"status": "ok"})


def tags(request: HttpRequest) -> JsonResponse:
    if request.method != "GET":
        return JsonResponse({"error": "GET method required."}, status=405)

    return JsonResponse(ALLOWED_TAGS, safe=False)


def suggest(request: HttpRequest) -> JsonResponse:
    if request.method != "GET":
        return JsonResponse({"error": "GET method required."}, status=405)

    requested_tags = request.GET.getlist("tag")

    unknown = [t for t in requested_tags if t not in ALLOWED_TAGS]
    if unknown:
        return JsonResponse({"error": f"Unknown tag(s): {', '.join(unknown)}"}, status=400)

    pool = MEALS
    if requested_tags:
        pool = [m for m in MEALS if all(t in m.get("tags", []) for t in requested_tags)]

    if not pool:
        return JsonResponse({"error": "No meals match the requested filters."}, status=400)

    try:
        r = requests.post(
            f"{CRYPTOPICK_URL}/pick/",
            json={"items": pool},
            timeout=20.0,
        )
        r.raise_for_status()
        selected = r.json()
    except Exception:
        selected = pool[0]

    return JsonResponse(selected, safe=False)
