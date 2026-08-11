from django.contrib import admin
from .models import Categories, Fooditems


# ==========================================================
#                       CATEGORY ADMIN
# ==========================================================

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):

    list_display = (

        "id",

        "name",

    )

    search_fields = (

        "name",

    )

    ordering = (

        "name",

    )


# ==========================================================
#                       FOOD ADMIN
# ==========================================================

@admin.register(Fooditems)
class FooditemsAdmin(admin.ModelAdmin):

    list_display = (

        "id",

        "name",

        "category",

        "price",

        "available",

    )

    list_filter = (

        "category",

        "available",

    )

    search_fields = (

        "name",

        "description",

    )

    list_editable = (

        "price",

        "available",

    )

    ordering = (

        "name",

    )