from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Fooditems, Categories

from django.shortcuts import render

def home(request):
    return render(request, "home.html" )


def contact(request):
    return render (request, 'contact.html')


def about(request):
    return render (request, 'about.html')


def menu(request):

    selected_category = request.GET.get("category")
    search = request.GET.get("search")

    foods = Fooditems.objects.all()

    if selected_category:
        foods = foods.filter(category_id=selected_category)

    if search:
        foods = foods.filter(name__icontains=search)

    categories = Categories.objects.all()

    context = {
        "foods": foods,
        "categories": categories,
        "selected_category": selected_category,
    }

    return render(request, "menu.html", context)


def food_detail(request, id):

    # Get the selected food
    food = get_object_or_404(
        Fooditems,
        id=id
    )

    # Get 3 other foods from the same category
    related_foods = Fooditems.objects.filter(
        category=food.category,
        available=True
    ).exclude(
        id=food.id
    )[:3]

    context = {
        "food": food,
        "related_foods": related_foods,
    }

    return render(
        request,
        "food_detail.html",
        context,
    )