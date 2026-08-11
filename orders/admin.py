from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem


# ==========================================================
#                       CART ADMIN
# ==========================================================

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = (

        "id",

        "user",

        "total_items",

        "total_price",

        "updated_at",

    )

    search_fields = (

        "user__username",

    )

    ordering = (

        "-updated_at",

    )


# ==========================================================
#                    CART ITEM ADMIN
# ==========================================================

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):

    list_display = (

        "id",

        "cart",

        "food",

        "quantity",

        "subtotal",

    )

    list_filter = (

        "food",

    )

    search_fields = (

        "food__name",

        "cart__user__username",

    )

    ordering = (

        "-added_at",

    )


# ==========================================================
#                      ORDER ADMIN
# ==========================================================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (

        "order_number",

        "user",

        "grand_total",

        "status",

        "payment_method",

        "payment_status",

        "created_at",

    )

    list_filter = (

        "status",

        "payment_method",

        "payment_status",

        "created_at",

    )

    search_fields = (

        "order_number",

        "user__username",

        "full_name",

        "phone",

    )

    ordering = (

        "-created_at",

    )

    readonly_fields = (

        "order_number",

        "created_at",

        "updated_at",

    )


# ==========================================================
#                   ORDER ITEM ADMIN
# ==========================================================

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (

        "order",

        "food_name",

        "quantity",

        "price",

        "subtotal",

    )

    search_fields = (

        "food_name",

        "order__order_number",

    )

    ordering = (

        "order",

    )